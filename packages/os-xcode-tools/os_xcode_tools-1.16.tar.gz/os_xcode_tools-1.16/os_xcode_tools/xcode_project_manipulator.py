from pbxproj import XcodeProject
import os
###########################################################################
#
# this module meant to inject/remove files in any xcode project
#
###########################################################################
from pbxproj.pbxextensions import ProjectFiles

SYSTEM_FRAMEWORK_PREFIX = 'System/Library/Frameworks'


def build_project(xcodeproj_path, pbxproj_path='project.pbxproj'):
    """
    call this initially. Will create the project object to work with.

    Args:
        xcodeproj_path -> the path to your xcodeproj file
        pbxproj_path -> the path to your pbxproj file (usually just project.pbxproj)
    """
    return XcodeProject.load(os.path.join(xcodeproj_path, pbxproj_path))


# will return the encloding folder of the project
def get_project_root(project):
    return project._source_root


# will create a group. if already exists, return it
def get_or_create_group(project, path_to_group):
    path = os.path.normpath(path_to_group)
    splatted_path = path.split(os.sep)
    last_group = None
    for i in splatted_path:
        last_group = project.get_or_create_group(i, parent=last_group)

        # last_group = project.get_or_create_group(i)

    return last_group
    # parent = project.get_or_create_group(parent_name)
    # return project.get_or_create_group(group_name, parent=parent)


# will add the references of a file into a group
# force = replace if exists
def add_file_to_group(project, file_path, group_obj, force=True):
    print(f'adding file: {file_path}...')
    project.add_file(file_path, force=force, parent=group_obj)


# will add the references of files into a group
# force = replace if exists
def add_arr_of_files_to_group(project, arr_of_files, group_obj, force=True):
    for file_path in arr_of_files:
        add_file_to_group(project, file_path, group_obj, force)


# # remove a whole group
# def remove_group(project, group_name):
#     return project.remove_group_by_name(group_name)

# remove a whole group
def remove_group(project, group):
    return project.remove_group_by_id(group._id)


def remove_file_from_group(project, group, file_name):
    for f in group.children:
        if f._get_comment() == file_name:
            project.remove_file_by_id(f)


# will remove all of the references of files from a given group
def clear_all_files_from_group(project, group_obj):
    while True:
        if len(group_obj.children) == 0:
            project.save()
            return
        for file in group_obj.children:
            project.remove_file_by_id(file)


# will add the ability to inject these array of extensions (add .zip, .xml etc...) to the copy sources.
# NOTICE: don't add extensions that are already defined in the ProjectFiles._FILE_TYPES, like: .plist or .swift files. This will override already desired behavior
def add_files_extensions_arr(extensions_arr):
    if '.plist' in extensions_arr:
        extensions_arr.remove('.plist')
    if '.swift' in extensions_arr:
        extensions_arr.remove('.swift')
    for ext in extensions_arr:
        ProjectFiles._FILE_TYPES[ext] = (ext[1:] + ext, u'PBXResourcesBuildPhase')


# will change the bundle id
def set_bundle_identifier(project, new_bundle_id):
    set_custom_flag(project, 'PRODUCT_BUNDLE_IDENTIFIER', new_bundle_id)


# will set a the product name
def set_product_name(project, new_product_name):
    set_custom_flag(project, 'PRODUCT_NAME', new_product_name)


# will set a custom flag to the project
def set_custom_flag(project, key, val):
    project.set_flags(key, val)


# will replace the info.plist file of the project.
# do this if you want to change the display name of the current project, for example.
def replace_info_plist_file(old_info_file, new_info_file):
    import os_file_handler.file_handler as fh
    fh.copy_file(new_info_file, old_info_file)


# save the changes in the project, otherwise your changes won't be picked up by Xcode
def save_changes(project):
    project.save()


def remove_framework_by_id(project, framework_id, delete=False, framework_path=None):
    """
    Will remove a framework from a project, by it's id.
    To find the id of a framework, call get_all_frameworks() and find the id from there.

    Args:
        project -> the xcode project
        framework_id -> your framework id
        delete -> set to true if you want to also delete the framework from the disk (caution: if the framework is only linked but not copied, leave this at False)
        framework_path -> set the path of the framework, if it's not a system one and you also want to delete it from the disk
    """

    project.remove_file_by_id(framework_id)

    if delete:
        import os_file_handler.file_handler as fh
        fh.remove_dir(framework_path)


def add_framework(project, framework_path, system_framework=False, parent_dir_name='Custom Frameworks'):
    """
    Will add a framework to a project

    Args:
        project -> the xcode project
        framework_path -> the path to the framework (if it's a system framework, just set it's name, like: AudioToolbox.framework. Otherwise, specify full path to the .framework file)
        system_framework -> set this to true if the framework is a system one
        parent_dir_name -> if you set 'copy' to true, specify the name of the parent dir in the project to which the library will be copied
    """

    if _is_pods_system_framework(framework_path):
        raise RuntimeError(f'No need to append the pods framework {framework_path}!')
    if system_framework:
        framework_dst = f'{SYSTEM_FRAMEWORK_PREFIX}/{framework_path}'
    else:
        import os_file_handler.file_handler as fh
        framework_dir_name = fh.get_dir_name(framework_path)
        frameworks_parent = os.path.join(project._source_root, parent_dir_name)
        fh.create_dir(frameworks_parent)
        framework_dst = os.path.join(frameworks_parent, framework_dir_name)
        if not fh.is_dir_exists(framework_dst):
            fh.copy_dir(framework_path, framework_dst)

    frameworks_group = project.get_or_create_group('Frameworks')
    from pbxproj.pbxextensions.ProjectFiles import FileOptions
    file_options = FileOptions(weak=True, embed_framework=not system_framework)

    project.add_file(framework_dst, parent=frameworks_group, tree='SDKROOT', force=False, file_options=file_options)


# will return all of the frameworks in the project. The returned value will be a list of dictionaries, each holds the name of the framework and its id
def get_all_framworks(project):
    framework_list = []
    potential_targets = project.objects.get_targets()
    for target in potential_targets.copy():
        for build_phase_id in target.buildPhases:
            build_phase = project.get_object(build_phase_id)
            for build_file_id in build_phase.files:
                build_file = project.get_object(build_file_id)
                file_ref = project.get_object(build_file.fileRef)
                if hasattr(file_ref, 'path'):
                    file_path = str(file_ref.path)
                    if file_path.endswith('.framework'):
                        if file_path not in framework_list:
                            framework_list.append({
                                'path': file_path,
                                'id': file_ref._id})

    return framework_list


# will add the dir and all of it's content to an xcode project
def add_dir(project, dir_src, dir_dst):
    from os_file_handler import file_handler as fh
    _append_dirs_recursively(project, [dir_src], dir_src, dir_dst, fh)


# the boilerplate code for adding directories
def _append_dirs_recursively(project, dirs_content, src_path_rel_root, dir_dst, fh):
    for idx_dir in dirs_content:

        stripped_root = idx_dir.replace(f'{src_path_rel_root}', '')
        if stripped_root.startswith('/'):
            stripped_root = stripped_root[1:]
        dst_path = os.path.join(dir_dst, stripped_root)

        print(f'creating dir: {dst_path}...')
        dir_group = get_or_create_group(project, dst_path)

        _append_dirs_recursively(project, fh.get_dir_content(idx_dir, False, True, False), src_path_rel_root, dir_dst, fh)
        for idx_file in fh.get_dir_content(idx_dir, False, False, True):
            add_file_to_group(project, idx_file, dir_group)


def set_frameworks(project, req_frameworks_dict_list):
    """
    Will set frameworks in a project.

    Args:
        project -> the xcode project
        req_frameworks_dict_list -> the list of frameworks you want to add. Each entry on the list should have a 'path' and a 'type'.
        The path is the path to the framework and the type is 'system' or 'custom'. In case of system framework, just set it's name in the path, like: UIKit.framework

    example:
        framework_dict_list = []
        framework_dict_list.append(
            {
                'type': 'system',
                'path': 'UIKit.framework',
            },
            {
                'type': 'custom',
                'path': '/local/path/to/AmazonFling.framework',
            },
        )
    """
    # uninstall all installed frameworks
    remove_all_frameworks(project)

    # install required frameworks
    for req_framework in req_frameworks_dict_list:
        add_framework(project, framework_path=req_framework['path'], system_framework=req_framework['type'] == 'system')


# will remove all of the currently installed frameworks from the project
# NOTICE: will not delete the pods framework
def remove_all_frameworks(project):
    installed_frameworks_dict_list = get_all_framworks(project)
    for installed_framework in installed_frameworks_dict_list:
        if _is_pods_system_framework(installed_framework['path']):
            continue
        delete_framework_from_disk = not is_system_framework(installed_framework['path'])
        remove_framework_by_id(project, installed_framework['id'], delete=delete_framework_from_disk, framework_path=installed_framework['path'])


# will return true if the framework is a system one
def is_system_framework(framework):
    return _is_pods_system_framework(framework) or framework.startswith(SYSTEM_FRAMEWORK_PREFIX)


# will check if the current framework is the pods framework
def _is_pods_system_framework(framework):
    return framework.startswith('Pods')
