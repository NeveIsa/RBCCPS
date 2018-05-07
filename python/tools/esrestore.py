import esbackup
import time

repo=esbackup.Repo()
repo.register()

repo.restore()

while True:
  time.sleep(1)
  repo.check_restore_progress("helloworld-2018-04-03")

