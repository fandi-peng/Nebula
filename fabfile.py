from fabric.api import local

def push():
    local("git add --all")
    local("git commit -m 'update'")
    local("git push origin master")
