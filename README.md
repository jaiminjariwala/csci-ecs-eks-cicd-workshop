# ECS and EKS CI/CD student workshop

Use official Visual Studio Code with GitHub Pull Requests, GitHub Actions and Kubernetes extensions.

The same dependency-free application is built once in Jenkins, pushed to ECR with an immutable Git commit tag, and deployed by digest to ECS Fargate and EKS. A release passes only when both applications report the same source commit and both platforms run the expected image digest.

Student flow: create the first GitHub commit, run baseline CI and deployment, clone locally in VS Code, create an enhancement branch, test it, push it, open a pull request, wait for CI, merge to main (the lab production branch), and observe Jenkins polling and deploying the merged revision.

AWS Academy restrictions: existing LabRole and LabInstanceProfile for ECS/Jenkins; the lab's existing LabEksClusterRole and LabEksNodeRole for EKS. No new IAM roles or GitHub AWS secrets. Jenkins has namespace-scoped EKS edit access. The administrator creates namespace workshop once. Jenkins is reached through SSM and listens on loopback only.

This repository is under active construction. The final guide and verified execution evidence will identify the tested steps and cleanup procedure. Do not leave the EKS control plane running between lab sessions: unlike EC2, it is billed while its worker nodes are stopped.
