# Implement the enhancement locally in VS Code

Start from the supplied starter at version 1.0.0. Create branch `enhancement/platform-comparison` using the status bar. Keep a copy of the completed example available in a separate VS Code window for reference.

1. In Explorer open `app/release.json`. Change version to `2.0.0` and set a message describing your comparison feature. Save.
2. In `app/server.py`, inside `response`, immediately before its final `return 404`, add the endpoint below. Keep indentation consistent.

```python
    if path == '/api/compare':
        return 200, {'comparison':[
            {'capability':'Application definition','ecs':'Task definition and ECS service','eks':'Kubernetes Deployment and Service'},
            {'capability':'Scheduling','ecs':'AWS ECS scheduler on Fargate','eks':'Kubernetes scheduler on managed EC2 nodes'},
            {'capability':'Recovery','ecs':'Deployment circuit breaker rollback','eks':'Readiness probes and explicit rollout undo'},
            {'capability':'Scaling','ecs':'Service desired task count','eks':'Deployment replica count'}]}
```

3. In `tests/test_app.py`, add a test inside `AppTests` before its `test_not_found` method:

```python
    def test_comparison_enhancement(self):
        status, data = app.response('/api/compare')
        self.assertEqual(status, 200)
        self.assertEqual(len(data['comparison']), 4)
        self.assertTrue(all(row['ecs'] and row['eks'] for row in data['comparison']))
```

4. Open the completed example `app/index.html` in the second VS Code window. Copy its contents into your local `app/index.html` and save. Read its refresh function: it fetches `/api/info`, `/healthz` and the new `/api/compare` endpoint. This supplied interface displays your new endpoint. Adapt the visible comparison text or add a capability and update the test count if your enhancement extends it.
5. Choose Terminal > Run Task > 4 Test application. Five tests must pass. Choose Preview local enhancement and inspect the page at http://127.0.0.1:18083. The starter server supports the PORT variable so it can use that task.
6. Source Control: inspect your local diff, Commit, Publish Branch. Create the PR, wait for CI and merge to main. Verify Jenkins and both deployed applications.

Explain the API, test and interface relationship in your submission. Merely changing a version number is not the full enhancement.
