# Git Exercises

## 1. Master

### Commands Used

```bash
git start master
git verify
```
THIS IS WHERE THE TASK BEGINS >_<
---

## 2. Commit One File

In this task, there are two files, but only one file needs to be committed.

Let the file be **A.txt**.

### Commands Used

```bash
git add A.txt
```

> Moves the  file `A.txt` from the working directory to the staging area.

```bash
git commit -m "Commit A.txt file"
```

> Saves all the committed changes locally with a descriptive message .

---

## 3. Commit One File of Two Currently Staged

Here both  files **A.txt** and **B.txt** are staged. Our objective here is to commit only **B.txt**.

### Commands Used

```bash
git start commit-one-file-staged
```

```bash
git reset A.txt
```

> Removes `A.txt` from the staging area while keeping the file unchanged.

```bash
git commit -m "Commit B.txt"
```

> Commits only `B.txt`.

```bash
git verify
```

> Verifies the exercise.

---

## 4. Ignore Them

### Objective

Here out objective is to ignore files and folders that should not be tracked by Git, such as compiled files, and libraries.

### Commands Used

```bash
echo "*.exe" > .gitignore
echo "*.o" >> .gitignore
echo "*.jar" >> .gitignore
echo "libraries/" >> .gitignore
```

> A file `.gitignore` is been created and then add rules to ignore `.exe`, `.o`, `.jar` files and the `libraries/` directory so that these files of such format be ignored .

```bash
git add .gitignore
```

> Takes the `.gitignore` file from working directory to staging area.

```bash
git commit -m "Add .gitignore rules"
```

> Saves the ignore rules in the repository by committing the changes.

```bash
git verify
```

> Verifies the exercise.

---

## 5. Chase Branch

### Objective

Bring the missing work from the `escaped` branch into the current branch.

### Commands Used

```bash
git merge escaped
```

> Merges the changes from the `escaped` branch into the current branch.

```bash
git verify
```

> Verifies the exercise.

---

## 6. Merge Conflict

### Objective

Resolve the merge conflict and commit the corrected version.

### Commands Used

```bash
git reset --hard HEAD~2
```

> Removes the last two commits and the drags the branch to the revious state.

```bash
echo "2+3=5" > equation.txt
```

>This command  Replaces the contents of `equation.txt` with the correct equation.

```bash
git add equation.txt
git commit -m "Resolve merge conflict"
```

> Commits the resolved changes with a discriptive message.

```bash
git verify
```

> Verifies the exercise.

---

## 7. Save Your Work

### Objective

To Temporarily save unfinished work, fix an urgent bug,restore the unfinished work and complete it.

### Commands Used

```bash
git stash
```

> Temporarily stores all uncommitted changes.

```bash
nano bug.txt
```

> Opens `bug.txt` to fix the bug.

```bash
git add bug.txt
git commit -m "Fix bug"
```

> Stages and commits the bug fix.

```bash
git stash pop
```

> Restores the previously stashed work.

```bash
echo "Finally, finished it!" >> bug.txt
```

> Adds the final line to complete the file.

```bash
git add .
git commit -m "Finish work"
```

> Stages all remaining changes and commits the completed work.

```bash
git verify
```

> Verifies the exercise.

---

## 8. Change Branch History

### Objective

Move the current branch commits on top of the `hot-bugfix` branch while maintaining a clean, linear history.

### Commands Used

```bash
git rebase hot-bugfix
```

> Replays the current branch commits on top of `hot-bugfix`branch .

```bash
git verify
```

> Verifies the exercise.

---

## 9. Remove Ignored

### Objective

Stop unwanted tracking of a file while keeping the file on the local machine.

### Commands Used

```bash
git rm --cached ignored.txt
```

> Removes `ignored.txt` from Git tracking without any deleting the local file.

```bash
git commit -m "Stop tracking ignored.txt"
```

> Saves the change in the Git history.

```bash
git verify
```

> Verifies the exercise.

---

## 10. Case-Sensitive Filename

### Objective

Renaming the name of the file if there is an error in case of the spelling or cases.

### Commands Used

```bash
git mv File.txt file.txt
```

> Renames the file and stages the changes automatically.

```bash
git commit -m "Rename File.txt to file.txt"
```

> Commit the changes made in the file name with a commit message .

```bash
git verify
```

> Verifies the exercise.

---

## 11. Fix Typo

### Objective

Update the previous commit by adding the missed changes without creating a new commit.

### Commands Used

```bash
nano file.txt
```

> Opens `file.txt` to correct the typo.

```bash
git add file.txt
```

> Staging the corret file to the staging area .

```bash
git commit --amend -m "Add Hello world"
```

> Replaces the previous commit with the updated changes and commit message.

```bash
git verify
```

> Verifies the exercise.


## 12.Forge-data

### Objective 
To forge the commit date.

### Commands Used

```bash
git commit --amend --date="1987-01-01" --no-edit
```
>Replaces the last commit , keeping the same commit message, but changes the author date to `1987-01-01`.

```bash
git verify
```

> Verifies the exercise.

## 13. Fix Old Typo

### Objective
Correcting the typo in the previous commit without creating a new commit and preserveing the clean history while resolving any merge conflicts.

### Commands Used 
```bash
git rebase -i HEAD~2
```

>It enables us to edti , modity and delecte the last two commits rewriting the commit history.

```bash
nano file.txt
```
> Opens the file `file.txt` to fix the typo.

```bash
git add file.txt
git commit --amend
git rebase --continue
```

>Stages the fix to the staging area , amends the target commit and then continues the rebase proceass.

>If merge conflict occures during the rebase then resolve the conflict markers , stage the files and then complete the rebase.

 
```bash
git verify
```

> Verifies the exercise.

## 14.Lost Commit

### Objective 

Recovering a lost commit that was accidentally overwritten and then restoring the branch pointer to its original state.

### Commands Used
 
```bash
git reflog
```

>It lists all the HEAD movements to identify the commit hash of the last comment prior to the amend action.

```bash
git reset --hard 9de4702	
```
>git reset moves the current branch pointer back to the original commit hash.


```bash
git verify
```

> Verifies the exercise.

## 15. Split Commit

### Objective 

Split the single comment containing multiple changes into seperate , smaller multiple commits 

### Commands Used 
```bash
git reset HEAD~1
```

>Undoes the last commit while keeping all the changes unstaged in the working directory.

```bash
git add first.txt
git commit -m "First part of split commit"        
```

>Stages the `first.txt` from working directory to staging area and then commits the first part of the text file .

```bash
git add second.txt  
git commit -m "First part of split commit"        
```

>Stages the `second.txt` from working directory to staging area and then commits the first part of the text file .

```bash
git verify
```

> Verifies the exercise.

## 16.Too Many Commits

### Objective 
Combining multiple small commits into commit so that the commit history stays clean. 

### Commands Used 

```bash
git rebase -i HEAD~2
```
> Opens a interactive rebase menu for the last 2 commits , change the pick to sqaush using the editor, and then save it .

```bash
git verify
```

> Verifies the exercise.

## 17.Make the file executable by default

### Objective
Updating a script's file permission in git so it is tracked as executable by default across checkouts.

### Commands used 
```bash
git update-index --chmod=+x script.sh
```
> Directly updates the file permission mode in git staging are to be executable .

```bash
git commit -m "Make script.sh executable"
```
> Commits the permission changes in the repo history .

```bash
git verify
```

> Verifies the exercise.

## 18.Commit part of work

### Objective 
Splitting the work into two separate commits even though all the changes were made in a single file.

### Commands used 
```bash
git add -p
```
> It stanges only the selected lines of the file.

```bash
git commit -m "Task 1"
```

> Commits the first part of the staging lines.

```bash
git add .
git commit -m "Remaining tasks"
```

>Staging and commiting all the remaining left out changes .

```bash
git verify
```

> Verifies the exercise.

## 19.Pick your features

### Objective 
Application of a specific feature onto the current branch resolving any merge conflicts.

### Commands used 
```bash
git cherry-pick feature-a
git cherry-pick feature-b
```

>Applies commit from `feature-a` and `featur-b` directly into the current branch .
```bash
git merge --squash feature-c
```

> Combines all the changes in `feature-c` into a single staging set.

```bash
nano program.txt
git add program.txt
git commit -m "Feature C"
```

> Resolves the conflicts in the file `program.txt` , state the file from the working directory to the stating area and the n commit change with a commit message.

```bash
git verify
```

> Verifies the exercise.


## 20.Rebase complex

### Objective 
Move the sub brach onto a new base branch while skipping the intermediate commits.

### Commands used 

```bash
git rebase --onto your-master issue-555 rebase-complex
```
>Replaces the base of the `rebase-complex` directly onto `your master` .

```bash
git verify
```

> Verifies the exercise.


## 21.Change order of commits

### Objective 
Swapping the order of the last two commits in the current brach .

###Change order of commits

```bash
git rebase -i HEAD~2
```
>This opens the interactive rebase menu , swap the positions of the commit in the editor and save them .

```bash
git verify
```

> Verifies the exercise.


## 22.Find Swearwords

### Objective 
Locating commits that has inappropriate languages and removing the offensive terms from the history.

### Commands used 

```bash
git log -S shit --oneline
```
>Searches for the exact commits where the word `shit` was added or removed.


```bash
git rebase -i --root
```
> Opens interactive rebase for the commit history to make the identified commit with `edit`.

```bash
git add words.txt
git commit --amend
git rebase --continue
```
>Replaces the offensive terms with flowers, amend the commit , and then continue the rebase .

```bash
git verify
```

> Verifies the exercise.


## 23.Find commit that has introduced bug

### Objective 
Locate the exact commit where the but base64 is introduced across hundreds of commits using binary search.

### Commands used 

```bash
git bisect start
git bisect bad HEAD
git bisect good 1.0
```

> Declaring the start point and the end point of the time line so that it only searches for the bug in the specific timeline .

```bash
git bisect run sh -c "openssl enc -base64 -A -d < home-screen-text.txt | grep -v jackass"
```
>Decodes data at each step automates evaluation to find out the error.

```bash
git push origin <COMMIT_ID>:find-bug
```
>Pushes the error hash to exercise remote branch for a verification .

```bash
git bisect reset
```
> cleans up the session state.

```bash
git verify
```

> Verifies the exercise.

# THE END ._.