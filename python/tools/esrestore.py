import esbackup

repo=esbackup.Repo()
repo.register()

repo.restore()
repo.check_restore_progress()
