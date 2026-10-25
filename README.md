# ECS and EKS CI/CD classroom workshop

Build one application in Jenkins and deploy the same immutable image to ECS Fargate and EKS. Use official Visual Studio Code for the local project, GitHub for review and CI, AWS Console for infrastructure, and Jenkins for delivery. `main` represents production **inside this disposable teaching lab**.

## Before class

Allow 45–60 minutes to prepare infrastructure; EKS creation is asynchronous. A 20-minute live presentation demonstrates an enhancement on a prepared baseline. Students build their own baseline outside that presentation window.

Install official VS Code, Git, Python 3.10+, AWS CLI v2, the AWS Session Manager plugin, and kubectl 1.35 from their official sources. In VS Code Extensions, install GitHub Pull Requests, GitHub Actions, and Kubernetes. GitHub sign-in for Source Control is required. This project has no Python package dependencies.

Use your own Learner Lab in us-east-1. Its existing roles must include LabRole, LabInstanceProfile, LabEksClusterRole and LabEksNodeRole. Role names may have lab-generated prefixes. A different lab policy can prevent this build; confirm these prerequisites before the live class.

## First GitHub version using VS Code

1. Extract the student starter folder and choose File > Open Folder in VS Code.
2. Choose Source Control > Initialize Repository. Review files; `.lab`, credentials and build artifacts must stay excluded.
3. Enter `Initial container workshop`, choose Commit, then Publish Branch > Publish to GitHub. Create your own private repository.
4. Open GitHub Actions and wait for the test workflow to pass. This is CI; it does not deploy AWS resources.

The instructor repository contains completed examples. Students should begin with the supplied 1.0.0 starter, not the completed enhancement.

## Create infrastructure in AWS Console

1. In VPC, identify the default VPC and two public subnets in different Availability Zones with internet routes and automatic public IPv4 assignment.
2. In IAM > Roles, copy the existing EKS cluster and node role ARNs. Do not create a replacement administrator role.
3. Open CloudFormation > Create stack > With new resources > Upload a template file. Select `infra/lab.yaml`.
4. Name the stack **csci-ecs-eks-cicd**. Select the VPC and both subnets. Enter your current public IPv4 address with `/32` as WorkstationCidr. Enter the two existing EKS role ARNs. Keep KubernetesVersion 1.35.
5. Review resources and submit. Wait for CREATE_COMPLETE, then record Outputs. This creates Jenkins EC2, ECR, ECS cluster, EKS cluster/node group, logs, and a private encrypted audit bucket. The pipeline creates the application service and deployment later.

The verified run initially created the stack through automation. A later AuditBucket-only update was performed and photographed through CloudFormation's interface. The screenshots do not imply that every initial creation click was executed through the console.

## Connect VS Code to the lab and prepare Jenkins

1. In Learner Lab choose AWS Details > AWS CLI. Copy the current temporary credential block into a local file named `.lab/credentials` using VS Code. Never commit it, photograph its values, or submit it. Refresh it after starting a new lab session.
2. Choose Terminal > Run Task > **1 Prepare Kubernetes namespace**. Wait for `Workshop namespace is ready`.
3. Choose Terminal > Run Task > **2 Prepare Jenkins** and enter your GitHub repository URL. The task runs the supplied setup through Systems Manager and creates a read-only repository key.
4. Open `.lab/github-readonly.pub`. In your GitHub repository choose Settings > Deploy keys > Add deploy key. Paste only this PUBLIC key. Leave Allow write access off.
5. AWS Console > Secrets Manager > **csci-jenkins-workshop** > Retrieve secret value contains the Jenkins username/password. Do not capture the value in screenshots.
6. Choose Terminal > Run Task > **3 Open private Jenkins tunnel**. Keep it running and open http://127.0.0.1:18080. Sign in with the generated credentials.
7. Open `container-delivery` > Build with Parameters. Keep CLOUD_EXTENSION off and choose Build. Read the stages and wait for SUCCESS.

Jenkins controls Docker on this dedicated lab host through its Docker socket. Use this arrangement only for the disposable teaching host and trusted repository contributors. Jenkins can read only its repository deploy key; AWS access uses the existing instance profile. EKS edit access is limited to namespace `workshop`. No GitHub AWS access keys are needed.

## Inspect the real baseline

Choose Terminal > Run Task > **5 Refresh deployed app previews**, then run **6 Open private ECS preview** and **7 Open private EKS preview** in separate task terminals. Keep the forwarding tasks open. Visit http://127.0.0.1:18081 and http://127.0.0.1:18082.

Both applications must display the expected release and commit. In Jenkins open the successful build > Artifacts > `verification.json`. A PASS requires the ECS/EKS application commits and actual image digests to match the image built from that commit. A green HTTP page alone is insufficient.

## Make and merge a local enhancement

1. In VS Code click the branch name > Create new branch. Enter `enhancement/platform-comparison`.
2. Edit `app/release.json` to version 2.0.0 and change the message. Implement an observable enhancement in the local application; the completed example adds `/api/compare` and a platform comparison view.
3. Choose Terminal > Run Task > **4 Test application**. All tests must pass. Use **Preview local enhancement** for the interface at http://127.0.0.1:18083.
4. In Source Control review the diff, enter a commit message, choose Commit and Publish Branch.
5. In GitHub choose Compare & pull request. Explain the change and test results. Review Files changed. Wait for all CI checks to pass, then Merge pull request > Confirm merge into `main`.
6. Jenkins polls `main` once per minute and deploys the merged commit. Open its console, confirm SUCCESS, and refresh deployed previews using task 5 after rollout.
7. Reopen both app pages and compare their commit with Jenkins `verification.json`. The local preview is development evidence; it does not prove deployment.

## Cloud Computing extension

In Jenkins > Build with Parameters turn **CLOUD_EXTENSION** on and choose Build. This intentionally deploys an unhealthy configuration in the teaching application, observes EKS rollout failure and explicit undo, observes ECS deployment circuit breaker recovery, scales both to two running copies, restores one, verifies identity, and writes an encrypted JSON report to the private audit bucket. Allow time for recovery rather than rerunning builds repeatedly.

Inspect the console stages, `cloud-extension.json`, ECS service deployment events, EKS deployment status, and S3 report. Use this run's actual results when writing your comparison. Do not claim a performance winner from a small teaching sample.

## Student submission

Submit the initial GitHub commit, enhancement PR and successful CI, local VS Code diff/test evidence, Jenkins successful deployment, both application pages, matching source/digest verification, and a 500–750 word ECS/EKS comparison. Discuss task definitions versus Kubernetes resources, compute responsibilities, access, recovery, scaling, complexity and cost drivers. Cloud Computing students additionally submit the recovery/scaling report and its private S3 object evidence.

Never submit credentials, Jenkins tokens, private SSH keys, or kubeconfig.

## Cleanup using interfaces

Preserve the evidence first. ECS > service > Update service: set desired tasks to zero, then delete this workshop service. EKS > cluster > Compute: delete the workshop node group (or let its CloudFormation stack deletion do that). In S3 empty only this workshop's audit bucket if deleting the stack. ECR: remove only workshop images if needed for repository deletion. CloudFormation > this stack > Delete. Review its events for DELETE_COMPLETE and resolve nonempty-resource errors. Delete the separately created `csci-jenkins-workshop` secret using its normal recovery window after it is no longer needed. Remove the workshop GitHub deploy key.

These cleanup steps destroy disposable lab resources; use only your workshop names and retain evidence before confirming deletion. Do not touch earlier PostgreSQL or Elasticsearch resources. EKS control-plane charges continue even while worker EC2 instances are stopped, so stopping Learner Lab is not complete cleanup.

## Resume and troubleshooting

Start Learner Lab, refresh `.lab/credentials`, and reopen the tunnel tasks. If a preview is stale after deployment, task 5 refreshes remote addresses. If localhost refuses the connection, check the corresponding task terminal and reopen its forwarding task. Do not open public ingress as a workaround.

If Jenkins fails, read the first failing stage. The verified development history includes fixes for an optional Jenkins plugin, a missing Docker CLI in a minimal image, and selecting a terminating old EKS pod. The final scripts include these corrections; failed earlier builds remain visible in history.

## Official references

- https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html
- https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html
- https://docs.aws.amazon.com/eks/latest/userguide/access-entries.html
- https://www.jenkins.io/doc/book/pipeline/jenkinsfile/
- https://code.visualstudio.com/docs/sourcecontrol/github
- https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html
