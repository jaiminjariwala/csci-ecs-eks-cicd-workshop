#!/usr/bin/env python3
"""Check local prerequisites without using AWS credentials or creating resources."""
import os,pathlib,re,subprocess,sys
private=pathlib.Path(__file__).resolve().parents[1]/'.lab'/'bin'
os.environ['PATH']=str(private)+os.pathsep+os.environ['PATH']
checks=[('Python',[sys.executable,'--version']),('Git',['git','--version']),('AWS CLI',['aws','--version']),('Session Manager plugin',['session-manager-plugin','--version']),('kubectl',['kubectl','version','--client'])]
failed=[]
for name,args in checks:
    try:
        r=subprocess.run(args,capture_output=True,text=True,timeout=20)
        output=(r.stdout+r.stderr).strip()
        print(('OK' if r.returncode==0 else 'CHECK')+'  '+name+'\n'+output+'\n',flush=True)
        if r.returncode:failed.append(name)
        elif name=='AWS CLI' and not output.startswith('aws-cli/2.'):
            print('Use AWS CLI version 2.');failed.append(name)
        elif name=='kubectl':
            version=re.search(r'Client Version: v(\d+)\.(\d+)',output)
            if not version or int(version[1])!=1 or abs(int(version[2])-35)>1:
                print('Use a kubectl client compatible with the 1.35 cluster.');failed.append(name)
    except (OSError,subprocess.TimeoutExpired):
        print('MISSING  '+name+' — follow its official installation link in the guide.\n',flush=True);failed.append(name)
if failed:raise SystemExit('Fix these tools, restart VS Code, and rerun: '+', '.join(failed))
print('All tools were found. AWS CLI v2 and kubectl compatibility with cluster 1.35 were checked. No AWS access was attempted.')
