#!/usr/bin/python
# coding=utf-8

import os
import uuid

import click
import yaml


@click.group()
def cli():
    pass


@cli.command()
@click.argument('name', default='')
def install(name):
    '''
    install dependency from meta/main.yml in local folder
    '''
    # Config
    temp_dir = '/tmp'
    location = os.getcwd()
    roles_env_path = os.environ.get('ROLES_FOLDER')
    roles_folder = './remote_roles'

    reqs_data = []
    meta_main_exist = True
    meta_reqs_exist = True

    if roles_env_path:
        roles_folder = roles_env_path
    # check ansible-galaxy exist
    if os.system("ansible-galaxy --version > /dev/null ") != 0:
        click.echo(click.style('✘ Ansible-galaxy not found!\n\
            Please install ansible on youre host or,\
            \nyou can manualy set path to ansible-galaxy bin,\n\
            use GALAXY_PATH env, or galaxy_path config options',
            fg='red'), err=True)
    click.echo(click.style(
        '✓ Ansible-galaxy bin found', fg='green'))

    # check meta/main.yml exist
    if not os.path.exists('%s/meta/main.yml' % location):
        click.echo(click.style(
            '✘ file meta/main.yml not found', fg='yellow'), err=True)
        meta_main_exist = False

    # check meta/requirements.yml exist
    if not os.path.exists('%s/meta/requirements.yml' % location):
        click.echo(click.style(
            '✘ file meta/requirements.yml not found', fg='yellow'), err=True)
        meta_reqs_exist = False

    if meta_main_exist:
        with open("%s/meta/main.yml" % location, 'r') as stream:
            try:
                deps_enable = True
                optional_deps_enable = True
                data = yaml.safe_load(stream)
                if data is None:
                    click.echo(click.style(
                        '? File meta/main.yml is empty\nSkipping install deps.', fg='yellow'))

                if 'dependencies' not in data or len(data['dependencies']) == 0:
                    click.echo(click.style(
                        '? Dependencies list is empty. Skipping ...', fg='yellow'))
                    deps_enable = False

                if 'optional_dependencies' not in data['galaxy_info'] or len(data['galaxy_info']['optional_dependencies']) == 0:
                    click.echo(click.style(
                        '? Optional dependencies list is empty. Skipping ...', fg='yellow'))
                    optional_deps_enable = False

                if optional_deps_enable:
                    reqs_data.append(data['galaxy_info']['optional_dependencies'])

                if deps_enable:
                    reqs_data.append(data['dependencies'])

                click.echo(click.style(
                    '✓ File meta/main.yml is valid', fg='green'))

            except yaml.YAMLError as exc:
                click.echo(click.style(exc, fg='red'), err=True)

        if meta_reqs_exist:
            with open("%s/meta/requirements.yml" % location, 'r') as stream:
                try:
                    data = yaml.safe_load(stream)
                    if data is None:
                        click.echo(click.style(
                            '? File meta/requirements.yml is empty\nSkipping install deps.', fg='yellow'))
                    elif type(data) == list:
                        click.echo(click.style(
                            '✓ File meta/requirements.yml is valid', fg='green'))
                        reqs_data.append(data)
                    else:
                        click.echo(click.style(
                            '✓ File meta/requirements.yml is not valid! file must be list', fg='yellow'))

                except yaml.YAMLError as exc:
                    click.echo(click.style(exc, fg='red'), err=True)

        if meta_main_exist or meta_reqs_exist:
            # Generate file reqs.yml
            uuid_var = str(uuid.uuid4())
            temp_ansible_reqs = "%s/ansible-%s.yml" % (temp_dir, uuid_var)

            flat_list = []
            for sublist in reqs_data:
                for item in sublist:
                    flat_list.append(item)

            # write data in install yaml file
            with open(temp_ansible_reqs, 'w') as yamlfile:
                yaml.dump({
                    'roles': flat_list
                }, yamlfile, default_flow_style=False)
            click.echo(click.style(
                '✓ The file with dependencies is ready\nInstalling to %s folder ...' % roles_folder, fg='green'))

            # Install from file reqs.yml
            if os.path.exists(temp_ansible_reqs):
                install_res = os.system('ansible-galaxy install -r %s -p %s --force' %
                                        (temp_ansible_reqs, roles_folder))
                if install_res == 0:
                    click.echo(click.style(
                        '✓ All dependencies were successfully installed\n\nHappy ansibling :)', fg='green'))
                    os.remove(temp_ansible_reqs)
                    exit(0)
                if install_res != 0:
                    click.echo(click.style(
                        '✘ An error occurred while installing dependencies', fg='red'), err=True)
                    os.remove(temp_ansible_reqs)
                    exit(1)


if __name__ == '__main__':
    cli()
