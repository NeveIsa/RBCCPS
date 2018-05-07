import esbackup

repo=esbackup.Repo()
repo.register()

repo.restore()

while true
do
sleep 1
repo.check_restore_progress()
done
