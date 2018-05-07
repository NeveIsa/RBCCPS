import esbackup
import time

repo=esbackup.Repo()
repo.register()

repo.restore()

while True:
  time.sleep(1)
  if repo.check_restore_progress()==0:
	"\n ---> RESTORE COMPLETED"
	exit(0)
  else:
	pass
	

