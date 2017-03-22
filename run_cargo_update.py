import os
import subprocess

def run_update(git_path, pkg):
    print("Running update for %s" % pkg.name)
    if os.path.isfile(os.path.join(git_path, 'mach')):
        mach_path = git_path + '/mach'
        args = [mach_path, 'cargo-update', '-p', pkg.name]
    else:  # Otherwise use default cargo update command
        cargo_bin_path = os.path.expanduser('~/.cargo/bin/cargo')
        args = [cargo_bin_path, 'update', '-p', pkg.name]
    print('This may take a moment...')
    print(args)
    cmd_out = None
    cmd_err = None
    cmd_out, cmd_err = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    print(cmd_err.decode('utf-8'))
    if 'is ambiguous.' in cmd_err.decode('utf-8'):  # If failure due to ambiguity, use precise version
        if os.path.isfile(os.path.join(git_path, 'mach')):
            mach_path = git_path + '/mach'
            args = [mach_path, 'cargo-update', '-p', (pkg.name + ':' + pkg.version)]
        else:  # Otherwise use default cargo update command
            cargo_bin_path = os.path.expanduser('~/.cargo/bin/cargo')
            args = [cargo_bin_path, 'update', '-p', (pkg.name + ':' + pkg.version)]
        print('Specifying version %s...' % pkg.version)
        print('This may take a moment...')
        print(args)
        cmd_out = None
        cmd_err = None
        cmd_out, cmd_err = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(cmd_err.decode('utf-8'))