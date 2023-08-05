# coding=utf-8
import datetime
import json
import os
import pathlib
from functools import partial
from multiprocessing.pool import Pool

import click
import humanize
from prettytable import PrettyTable

from rebotics_sdk.advanced import remote_loaders
from rebotics_sdk.cli.common import shell, configure, roles
from .renderers import format_full_table
from .utils import ReboticsCLIContext, app_dir, pass_rebotics_context, read_saved_role, process_role
from ..advanced.flows import FileUploadError, download_vrcdb_file, ReboticsClassificationDatabase
from ..advanced.packers import ClassificationDatabasePacker, ClassificationDatabaseException, \
    DuplicateFeatureVectorsException, VirtualClassificationDatabasePacker
from ..constants import RCDB
from ..providers import AdminProvider, RetailerProvider, sleep
from ..providers.facenet import FacenetProvider
from ..utils import Timer


@click.group()
@click.option('-f', '--format', default='table', type=click.Choice(['table', 'id', 'json']), help='Result rendering')
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode')
@click.option('-c', '--config', type=click.Path(), default='admin.json', help="Specify what config.json to use")
@click.option('-r', '--role', default=lambda: read_saved_role('admin'), help="Key to specify what admin to use")
@click.version_option()
@click.pass_context
def api(ctx, format, verbose, config, role):
    """
    Admin CLI tool to communicate with dataset API
    """
    process_role(ctx, role, 'admin')
    ctx.obj = ReboticsCLIContext(
        role,
        format,
        verbose,
        os.path.join(app_dir, config),
        provider_class=AdminProvider
    )


def get_retailer_version_task(retailer_dict):
    retailer_provider = RetailerProvider(host=retailer_dict['host'], retries=1, timeout=5)
    try:
        response = retailer_provider.version()
        version = response['version']
        uptime = humanize.naturaldelta(datetime.timedelta(seconds=int(response['uptime'])))
    except Exception:
        version = 'not working'
        uptime = '---'

    d = [
        retailer_dict['codename'],
        retailer_dict['title'],
        version,
        uptime,
        retailer_dict['host'],
    ]
    return d


@api.command()
@click.argument('retailer')
@pass_rebotics_context
def configurations(ctx, retailer):
    """
        Fetch retailer configurations variables
    """
    try:
        res = ctx.provider.get_configurations(retailer)
        ctx.format_result(res)
    except Exception as exc:
        raise click.ClickException(exc)


@api.command()
@click.option('-n', '--notify', is_flag=True)
@click.option('-d', '--delay', type=click.INT, default=60)
@pass_rebotics_context
def retailer_versions(ctx, notify, delay):
    """Fetch retailer versions and their meta information"""
    click.echo("For better experience use: \n"
               "https://versions.fyn.rocks/ and https://tracker.fyn.rocks/")

    if notify:
        if ctx.verbose:
            click.echo('Using notify option', err=True)

        try:
            from pynotifier import Notification
            Notification(
                title='Subscribed to the notifications',
                description='You will receive notifications for retailer updates',
            ).send()
        except ImportError:
            raise click.ClickException("You can't use notify function")

    provider = ctx.provider
    if ctx.verbose:
        click.echo('Fetching info from rebotics admin.', err=True)
    retailers = provider.get_retailer_list()
    prev_results = []
    results = []
    pool = Pool(len(retailers))

    while True:
        try:
            if ctx.verbose:
                click.echo('Fetching the retailer versions', err=True)
            results = pool.map(get_retailer_version_task, retailers)

            if not notify:
                break

            for prev_result in prev_results:
                retailer_codename = prev_result[0]
                previous_version = prev_result[2]
                for result in results:
                    if result[0] == retailer_codename:
                        current_version = result[2]
                        if previous_version != current_version:
                            notification_message = 'Retailer {} updated from version {} to {}'.format(
                                retailer_codename,
                                previous_version,
                                current_version
                            )
                            click.echo(notification_message)
                            Notification(
                                title=notification_message,
                                description='Current uptime is: {}'.format(result[3]),
                                duration=30,
                                urgency=Notification.URGENCY_CRITICAL,
                            ).send()
            del prev_results
            prev_results = results
            sleep(delay)
        except KeyboardInterrupt:
            break

    table = PrettyTable()
    table.field_names = ['codename', 'title', 'version', 'uptime', 'host']
    for result in results:
        table.add_row(result)
    click.echo(table)


@api.command()
@click.argument('retailer')
@pass_rebotics_context
def models(ctx, retailer):
    """
        Fetch and display retailer NN configurations
    """
    try:
        ctx.format_result(
            ctx.provider.get_retailer_tf_models(codename=retailer)
        )
    except Exception as exc:
        raise click.ClickException(exc)


@api.command()
@click.option('-r', '--retailer', help='Retailer codename')
@click.option('-u', '--facenet-url', help='Facenet service URL')
@click.argument('image_url')
@pass_rebotics_context
def extract_feature_vectors(ctx, retailer, facenet_url, image_url):
    """Fetches latest configuration of neural model for retailer by it's ID and Secret key;
    Sends image to facenet to load model into state."""
    models = ctx.provider.get_retailer_tf_models(codename=retailer)

    facenet_model = models['facenet_model']
    if ctx.verbose:
        click.echo("Facenet model: %s" % facenet_model['codename'])

    facenet_provider = FacenetProvider(facenet_url)
    feature_extractor = partial(
        facenet_provider.extract_from_image_url,
        model_path=facenet_model['data_path'],
        index_path=facenet_model['index_path'],
        meta_path=facenet_model['meta_path'],
    )

    with Timer() as t:
        result = feature_extractor(image_url)
        click.echo(result)

    if ctx.verbose:
        click.echo("Elapsed: %s seconds" % t.elapsed_secs)


@api.command()
@click.option('-r', '--retailer', help='Retailer')
@click.option('-u', '--facenet-url', help='Facenet service URL')
@click.argument('image_url')
@click.argument('bounding_boxes', type=click.File())
@pass_rebotics_context
def extract_feature_vectors_for_boxes(ctx, retailer, facenet_url, image_url, bounding_boxes):
    """Fetches latest configuration of neural model for retailer by it's ID and Secret key;
    Sends keyframe image url and list of bounding boxes to facenet to load model into state."""
    models = ctx.get_retailer_tf_models(codename=retailer)

    facenet_model = models['facenet_model']
    if ctx.verbose:
        click.echo("Facenet model: %s" % facenet_model['codename'])

    boxes = json.load(bounding_boxes)
    assert isinstance(boxes, list), "Need to supply list of bounding boxes"

    facenet_provider = FacenetProvider(facenet_url)
    feature_extractor = partial(
        facenet_provider.extract_from_keyframe,
        model_path=facenet_model['data_path'],
        index_path=facenet_model['index_path'],
        meta_path=facenet_model['meta_path'],
    )

    with Timer() as t:
        result = feature_extractor(keyframe_url=image_url, bboxes=boxes)
        click.echo(result)

    if ctx.verbose:
        click.echo("Elapsed: %s seconds" % t.elapsed_secs)


@api.command()
@click.argument('retailer', type=click.STRING)
@click.argument('url', type=click.STRING)
@pass_rebotics_context
def set_retailer_url(ctx, retailer, url):
    try:
        ctx.provider.update_host(retailer, url)
    except Exception as exc:
        raise click.ClickException(str(exc))
    else:
        click.echo('Set new host for retailer %s' % retailer)


@api.command()
@click.option('-r', '--retailer', help="Retailer codename", prompt=True)
@click.option('-m', '--model', help="Model codename", prompt=True)
@click.option('-i', '--images', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('-l', '--labels', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('-f', '--features', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('-c', '--check-duplicates', is_flag=True, help="MD5 checker simple")
@pass_rebotics_context
def pack_and_import_classification_db(ctx, retailer, model, images, labels, features, check_duplicates):
    """Pack classification database to single .rcdb file and import it to the Rebotics Admin

\b
db/
├── custom_folder
│   ├── image_2.png
│   └── image_1.png
├── features.txt
└── labels.txt

    It is a single step command with equivalent of running two commands:

admin pack-classification-db --features features.txt --labels labels.txt --images ./custom_folder/ --target classification.rcdb

admin import_classification_db --retailer delta --model test_code classification.rcdb
    """
    ext = ClassificationDatabasePacker.extension
    with ctx.provider.rcdb.import_flow(retailer, model, ext) as flow:
        if ctx.verbose:
            click.echo("Creating import request: \n"
                       "retailer: {}\n"
                       "model: {}\n"
                       "extension: {}".format(retailer, model, ClassificationDatabasePacker))

        packer = ClassificationDatabasePacker(destination=None, progress_bar=True, check_duplicates=check_duplicates)
        if ctx.verbose:
            click.echo("Packing from provided values: \n"
                       "labels: {labels} \n"
                       "features: {features} \n"
                       "images: {images}".format(labels=labels, features=features, images=images))

        try:
            packed = packer.pack(labels, features, images)
            packed.seek(0)
        except DuplicateFeatureVectorsException as exc:
            handle_duplicates(ctx, exc.duplicates)
            raise click.ClickException(str(exc))
        except ClassificationDatabaseException as exc:
            raise click.ClickException(str(exc))

        if ctx.verbose:
            click.echo("Import request: {}".format(flow.import_request))

        try:
            flow.upload_file(packed, progress_bar=True)
        except FileUploadError as exc:
            click.echo(str(exc))
            raise

        click.echo("Import completed. Reference database id: {}".format(flow.import_request['id']))


@api.command()
@click.option('-r', '--retailer', help="Retailer codename", prompt=True)
@click.option('-m', '--model', help="Model codename", prompt=True)
@click.argument('filepath', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@pass_rebotics_context
def import_classification_db(ctx, retailer, model, filepath):
    """Import rcdb file to Rebotics Admin. Example usage:

    admin import_classification_db --retailer delta --model test_code classification.rcdb

    """
    extension = os.path.split(filepath)[-1].split('.')[-1]
    if ctx.verbose:
        click.echo("Creating import request: \n"
                   "retailer: {}\n"
                   "model: {}\n"
                   "extension: {}".format(retailer, model, extension))

    with ctx.provider.rcdb.import_flow(retailer, model, extension) as flow:
        if ctx.verbose:
            click.echo("Import request: {}".format(flow.import_request))
        with open(filepath, 'rb') as packed:
            flow.upload_file(packed, progress_bar=True)

    click.echo("Import completed. Reference database id: {}".format(flow.import_request['id']))


def handle_duplicates(ctx, duplicates):
    unpacked = [
        [
            {
                'id': entry.index,
                'label': entry.label,
                'filename': entry.filename
            }
            for entry in group
        ] for group in duplicates
    ]
    if ctx.format == 'json':
        click.echo(json.dumps(unpacked, indent=2))
    elif ctx.format == 'table':
        for group in unpacked:
            format_full_table(group)
    elif ctx.format == 'id':
        click.echo("Duplicate id. New line separated for group; space separated inside of the group:")
        for group in duplicates:
            click.echo(" ".join([str(entry.index) for entry in group]))
    else:
        for group in duplicates:
            for entry in group:
                click.echo("{entry.index} {entry.label} {entry.filename}".format(entry=entry))
            click.echo('=' * 100)


@api.command()
@click.option('-i', '--images', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('-l', '--labels', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('-f', '--features', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('-c', '--check-duplicates', is_flag=True, help="MD5 checker simple")
@click.argument('target', type=click.Path(exists=False, file_okay=True, dir_okay=True), default='.')
@pass_rebotics_context
def pack_classification_db(ctx, images, labels, features, target, check_duplicates):
    """Pack classification database to single .rcdb file

\b
db/
├── custom_folder
│   ├── image_2.png
│   └── image_1.png
├── features.txt
└── labels.txt

    Example usage:
        admin pack-classification-db --features features.txt --labels labels.txt --images ./custom_folder/ --target classification.rcdb

    """
    target = pathlib.Path(target)
    if target.is_dir():
        target = target / "classification_db{}.{}".format(
            datetime.datetime.now().strftime('%Y-%m-%dZ%H%M'),
            ClassificationDatabasePacker.extension
        )
    packer = ClassificationDatabasePacker(
        destination=target,
        progress_bar=True,
        check_duplicates=check_duplicates
    )
    if ctx.verbose:
        click.echo("Packing from provided values: \n"
                   "labels: {labels} \n"
                   "features: {features} \n"
                   "images: {images}".format(labels=labels, features=features, images=images))
    try:
        packed = packer.pack(labels, features, images)
    except DuplicateFeatureVectorsException as exc:
        handle_duplicates(ctx, exc.duplicates)
        raise click.ClickException(str(exc))
    except ClassificationDatabaseException as exc:
        raise click.ClickException(str(exc))
    click.echo('Written to {}'.format(packed))


@api.group()
def rcdb_group():
    pass


@rcdb_group.command()
@click.option('-r', '--retailer', help="Retailer codename", prompt=True)
@click.option('-m', '--model', help="Model codename", prompt=True)
@click.option('-c', '--concurrency', type=int, default=4)
@click.argument('target', type=click.Path(exists=False, file_okay=False, dir_okay=True), default='.')
@pass_rebotics_context
def backup_and_download_rcdb(ctx, retailer, model, target, concurrency):
    """
    CLI command to trigger the upload
    """
    rcdb = ReboticsClassificationDatabase(ctx.provider)
    # a flow that will request to do a backup of the retailer + model from the Admin
    res = rcdb.create(retailer, model)
    id_ = res['id']

    # next flow wait for it to be processed calling the function to be done or not every N minutes
    with Timer() as t:
        while True:
            res = rcdb.get(id_)
            if res['status'] == RCDB.EXPORT_DONE:
                file_url = res['backup']
                break
            if res['status'] == RCDB.EXPORT_ERROR:
                raise click.ClickException("Creating and RCDB file failed")
            sleep(5)

    click.echo("Elapsed time: {}".format(t.elapsed_secs))

    # flow that will download the rcdb file
    file_io = remote_loaders.download(file_url, progress_bar=True)

    # next flow that will unpack rcdb into target directory
    target = pathlib.Path(target) / "rcdb_{}_{}_{}".format(retailer, model, id_)

    packer = VirtualClassificationDatabasePacker(source=file_io)
    download_vrcdb_file(packer, target, concurrency=concurrency)


@rcdb_group.command()
@click.option('-c', '--concurrency', type=int, default=4)
@click.argument('target', type=click.Path(exists=False, file_okay=False, dir_okay=True), default='.')
@click.argument('backup_ids', type=click.INT, nargs=-1)
@pass_rebotics_context
def download_rcdb(ctx, backup_ids, target, concurrency):
    """
    Download rcdb by id
    :param ctx:
    :param backup_ids:
    :param target:
    :param concurrency:
    :return:
    """
    rcdb = ReboticsClassificationDatabase(ctx.provider)
    target = pathlib.Path(target)

    for backup_id in backup_ids:
        res = rcdb.get(backup_id)

        file_url = res['backup']
        retailer = res['retailer']
        model = res['facenet_model']

        # flow that will download the rcdb file
        file_io = remote_loaders.download(file_url, progress_bar=True)

        # next flow that will unpack rcdb into target directory
        download_folder = target / "rcdb_{}_{}_{}".format(retailer, model, backup_id)

        packer = VirtualClassificationDatabasePacker(source=file_io)
        download_vrcdb_file(packer, download_folder, concurrency=concurrency)


@rcdb_group.command()
@click.option('-c', '--concurrency', type=int, default=4)
@click.argument('backup', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument('target', type=click.Path(exists=False, file_okay=False, dir_okay=True), default='.')
@pass_rebotics_context
def unpack_rcdb(backup, target, concurrency):
    # TODO: check by filename and extension
    packer = VirtualClassificationDatabasePacker(source=backup)
    download_vrcdb_file(packer, target, concurrency=concurrency)


api.add_command(shell, 'shell')
api.add_command(roles, 'roles')
api.add_command(configure, 'configure')
