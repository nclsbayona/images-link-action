from github import Github, InputGitAuthor
from os import environ
from Tree import *

repository=environ["REPOSITORY"]
github_token=environ['GITHUB_TOKEN']
github_user=Github(github_token)
repo=github_user.get_repo(repository)
old_readme=repo.get_readme()
lines=[line.decode() for line in old_readme.decoded_content.splitlines()]
tree:Tree=None

def makeRecursiveDirFileTree(path="."):
    tree=dict()
    from os.path import abspath, isfile, splitext
    absolute_path=abspath(path)
    if isfile(absolute_path):
        # This isn't a directory and therefore, shouldn't continue looking through it
        tree=splitext(absolute_path)[-1] or "No extension"
    else:
        # This is a directory and therefore have to look through it
        from os import listdir
        for archive in listdir(absolute_path):
            directory=f"{absolute_path}/{archive}"
            tree[archive]=makeRecursiveDirFileTree(directory)

    return tree

def lookForImages(dirTree, images=list(), path="", extensions=(".png", ".jpg", ".jpeg")) -> list:
    for archive in dirTree:
        if (not archive.startswith(".") and isinstance(dirTree[archive], dict)):
            # A directory I should inspect
            lookForImages(dirTree=dirTree[archive], images=images, path=f"{path}/{archive}" if len(path) > 0 else f"{archive}", extensions=extensions)
        elif (not isinstance(dirTree[archive], dict) and dirTree[archive].startswith(extensions)):
            # An image
            images.append(f"{path}/{archive}" if len(path) > 0 else f"{archive}")

    return images

def decideStringForReadme(file:str) -> str:
    file_id=file.split('.')[0][-1]
    end_text=f"![#{file_id}]({file})"
    return end_text
    
def makeOldReadmeTree():
    global tree, lines
    node: Node=None
    new_node: Node=None
    for i, line in enumerate (lines):
        if (tree is None):
            if (not line.startswith("# ")):
                continue
            else:
                node=Node(line, i)
                tree=Tree(node)
                continue
        elif (len(line)>1 and (line.startswith(('#','-', '![')))):
            new_node=Node(line, i)
            if (not node.getLevel()<new_node.getLevel()):
                level_desired=new_node.getLevel()-1
                while(node.getLevel()>=new_node.getLevel() and level_desired>0):
                    node=tree.getLevelLatest(level_desired)
                    level_desired-=1
                
            node.addChild(new_node)
            node=new_node

def searchForImagesInOldReadme():
    global tree
    makeOldReadmeTree()
    ret=[]
    print ("Old images:")
    for image in tree.getImages():
        try:
            ret.extend(image)
        except:
            ret.append(image)
        print(image)
    print(len(ret))
    return ret

def decideNewImages():
    images=list(map(decideStringForReadme, lookForImages(makeRecursiveDirFileTree())))
    old_images=[node.getData() for node in searchForImagesInOldReadme()]
    for image in (old_images):
        try:
            images.remove(image)
        except:
            pass
    return images

def makeData(image_data):
    cont=2
    ret=[]
    for image in (image_data[:-2]):
        ret.append(str('#'*cont+' '+image))
        cont+=1
    ret.append(f'- {image_data[-2]}')
    ret.append(f'![#{image_data[-1].split(".")[0]}]({"/".join(image_data)})')
    return ret

def separateImage(image:str):
  separated=list(''.join(image.split('(')[-1]).replace(')','').split('/'))
  return separated


def main():
    new_images=list(map(separateImage, decideNewImages()))
    to_add=list(map(makeData, new_images))
    print("New images:")
    for img in to_add:
        tree.addNewImage(img)
        print(img)
    print()
    ordered=tree.orderNodesByLineNumber()
    readme=[]
    print ("Ordered\n", [o.__str__() for o in ordered])
    for _ in range(ordered[-1].getLine()+1):
        readme.append("")
    for data in ordered:
        readme[data.getLine()]=data.getData()
    new_readme="\n".join(readme)
    print("Readme\n",readme,"\nNew readme\n", new_readme)
    repo.update_file(
        path=old_readme.path,
        message="Updated the README file",
        content=new_readme,
        sha=old_readme.sha,
        committer=InputGitAuthor("Auto_Update-Bot", "github-actions[bot]@users.noreply.github.com"),
    )

if __name__=="__main__":
    main()