#!/home/annyterfect/anaconda3/envs/py36/bin/python
#-*- coding: utf-8 -*-
import sqlite3
import os
from fire import Fire
from time import sleep
from subprocess import check_output
from syslog import openlog, syslog
openlog('[Cloudreve Trash Cleaner]')

def log(msg):
	msg = str(msg)
	syslog(msg)
	print(msg)

def main(work_dir=''):
	while True:
		clean(work_dir)
		sleep(5)

def clean(work_dir):
	os.chdir(work_dir)
	files = check_output(['find', f'{work_dir}/uploads/1/']).decode().split('\n')[:-1]
	paths = ['/'.join(file.split('/')[:-1]) for file in files]
	names = [file.split('/')[-1] for file in files]
	pre_names = ['_'.join(name.split('_')[:2]) for name in names]
	names = ['_'.join(name.split('_')[2:]) for name in names]
	for path, pre_name, name in zip (paths, pre_names, names):
		if '._' in name and name.replace('._', '', 1) in names or '.DS_Store' in name:
			full_path = f'{path}/{pre_name}_{name}'
			log(f'cleaning {full_path}')
			check_output(['rm', full_path])

	conn = sqlite3.connect('cloudreve.db')
	cursor = conn.cursor()

	cursor.execute('SELECT id, source_name FROM files;')
	db_files = cursor.fetchall()
	for (fid, source_name) in db_files:
		if not(os.path.exists(source_name)):
			cursor.execute(f'DELETE FROM files WHERE id={fid}')
			log(f'cleaning {source_name}')
	
	cursor.execute('DELETE FROM files WHERE instr(name, ".DS_Store")>0')
	cursor.execute('DELETE FROM files WHERE name in (SELECT f2.name FROM files f1, files f2 WHERE f2.name="._"||f1.name)')

	conn.commit()
	conn.close()


if __name__ == '__main__':
	Fire(main)