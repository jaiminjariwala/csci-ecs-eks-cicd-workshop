# Instructor live demonstration

Friday October 30 2026. Prepare the baseline before class. EKS creation and the full recovery extension do not fit a 20-minute presentation.

## Preparation

Start Learner Lab 45–60 minutes early. Check budget and temporary credentials. Confirm the stack, Jenkins and EKS node are ready. Run a baseline build and save verification. Open private Jenkins, ECS and EKS tunnels using VS Code tasks. Keep task terminals running. Open both apps, GitHub and VS Code before projecting. Hide all secrets and AWS Details.

## Twenty minute sequence

- Minutes 0–2: both baseline apps and matching source in Jenkins verification.
- Minutes 2–5: VS Code Source Control > Create branch. Edit release message and explain the comparison enhancement.
- Minutes 5–8: Terminal > Run Task > Test application. Review diff, Commit and Publish Branch.
- Minutes 8–11: GitHub PR > Files changed > passed CI > Merge > Confirm merge into main.
- Minutes 11–16: Jenkins detects main. Show Test, Build and push, Deploy ECS, Deploy EKS and Verify. Explain asynchronous waits; use a prepared successful run if rollout exceeds the slot, clearly identifying it as an earlier verified run.
- Minutes 16–19: refresh previews task, show both new apps and identical commit/digest. Compare ECS task definition and EKS Deployment in AWS Console.
- Minute 19–20: submission, Cloud Computing extension and cleanup.

## Cloud Computing follow-up

Show Build with Parameters > CLOUD_EXTENSION. Run outside the short presentation. Inspect failed health checks, explicit Kubernetes undo versus ECS circuit breaker recovery, scale-to-two evidence and private S3 JSON report. The final recovery and identity checks must pass.

## Demonstration fallback

Do not claim queued/failed builds are successful. Use stored screenshots and verified JSON while explaining a lab outage or expired session. Refresh credentials and tunnels before resuming. Never project credential values.
