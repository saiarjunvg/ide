# ide
Follow the following steps to set up your first project
1. clone project (assuming that you have an github account, if not, create one :)) 
`git clone https://github.com/chiihiro1608/ide.git`

2. Install python
https://tutorial.djangogirls.org/en/python_installation/

3. Install code editor
Use Pycharm or VSCode, but i use Pycharm because it is faster, but it doesnt support front end

4. create the virtual environment
cd to ide folder
`python3 -m venv myvenv`
activate virtual env
`source myvenv/bin/activate` (use tab to auto fill)

5. Install packages
First, you have to install pip
`python3 -m pip install --upgrade pip`
Then, install all packages/dependencies from requirement.txt file
`pip install -r requirements.txt`

NOTE
* To deactivate virtual env
`deactivate`
* Everytime you install something into the project, you have to update the requirement.txt by running this
`pip freeze requirement.txt`
copy all of it and replace the exiting requirement.txt

Some basic git commands
* to check how many branch in your local
`git branch`
* to go to a different branch
`git checkout master` -> this go to master
* to create a new branch from master. Always pull the latest master first
`git pull origin master`
`git checkout -b branchname`
* if you are in the middle of something, and you dont want to commit it
`git stash` and then you can switch to another branch
* then switch back to your branch
`git stash pop`
* to check status
`git status`
* to add file
`git add 'filename'`
* to commit
`git commit -m "message here"`
* to push
`git push`
* to checkout the file that you dont want to commit
`git checkout file`
* if you have already added the file, but you change your mind and dont want to commit it
`git status`
`git reset HEAD file`
* merge master to your branch. PLEASE DON'T USE MERGE. USE GIT MERGE REBASE
`git pull origin --rebase master`
if there is conflict with master, you have to fix it
after fixing it
```
git status
git add filename
git rebase --continue
git push -f
```
git push -f is force push
if you dont want to fix the conflict, you can abort it
`git rebase --abort`
* clean up your local branches
`git branch -D branchname` to delete branch
HIGHLY RECOMMEND DO NOT TO branch off branch. Example, feature/b is branched off from feature/a (of course, feature/a is not master). In theory, you can do that, but you are not master of git, it can make the mess
master 
       feature/a
                 feature/b


References
* https://tutorial.djangogirls.org/en/
* https://www.atlassian.com/git/tutorials/learn-git-with-bitbucket-cloud
