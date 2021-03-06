"""
Tests for RunCaseVersion model.

"""
from tests import case



class RunCaseVersionTest(case.DBTestCase):
    def test_unicode(self):
        c = self.F.RunCaseVersionFactory(
            run__name="FF10", caseversion__name="Open URL")

        self.assertEqual(unicode(c), u"Case 'Open URL' included in run 'FF10'")


    def test_bug_urls(self):
        """bug_urls aggregates bug urls from all results, sans dupes."""
        rcv = self.F.RunCaseVersionFactory.create()
        result1 = self.F.ResultFactory.create(runcaseversion=rcv)
        result2 = self.F.ResultFactory.create(runcaseversion=rcv)
        self.F.StepResultFactory.create(result=result1)
        self.F.StepResultFactory.create(
            result=result1, bug_url="http://www.example.com/bug1")
        self.F.StepResultFactory.create(
            result=result2, bug_url="http://www.example.com/bug1")
        self.F.StepResultFactory.create(
            result=result2, bug_url="http://www.example.com/bug2")

        self.assertEqual(
            rcv.bug_urls(),
            set(["http://www.example.com/bug1", "http://www.example.com/bug2"])
            )


    def test_environment_inheritance(self):
        """RCV gets intersection of run and caseversion environments."""
        envs = self.F.EnvironmentFactory.create_set(
            ["OS", "Browser"],
            ["Linux", "Firefox"],
            ["Linux", "Chrome"],
            ["OS X", "Chrome"],
            )

        rcv = self.F.RunCaseVersionFactory.create(
            run__environments=envs[:2],
            caseversion__environments=envs[1:])

        self.assertEqual(rcv.environments.get(), envs[1])

        # only happens when first created, not on later saves

        rcv.environments.clear()
        rcv.save()

        self.assertEqual(rcv.environments.count(), 0)


    def test_inherits_env_removal_from_run(self):
        """RCV inherits env removal from test run."""
        envs = self.F.EnvironmentFactory.create_full_set(
            {"OS": ["OS X", "Linux"]})
        r = self.F.RunFactory(environments=envs)
        cv = self.F.CaseVersionFactory(environments=envs)
        rcv = self.F.RunCaseVersionFactory(run=r, caseversion=cv)

        r.remove_envs(envs[0])

        self.assertEqual(set(rcv.environments.all()), set(envs[1:]))


    def test_does_not_inherit_env_addition_on_run(self):
        """RCV does not inherit env addition on test run."""
        envs = self.F.EnvironmentFactory.create_full_set(
            {"OS": ["OS X", "Linux"]})
        r = self.F.RunFactory(environments=envs[1:])
        cv = self.F.CaseVersionFactory(environments=envs)
        rcv = self.F.RunCaseVersionFactory(run=r, caseversion=cv)

        r.add_envs(envs[0])

        self.assertEqual(set(rcv.environments.all()), set(envs[1:]))


    def test_inherits_env_removal_from_productversion(self):
        """RCV inherits env removal from product version."""
        envs = self.F.EnvironmentFactory.create_full_set(
            {"OS": ["OS X", "Linux"]})
        pv = self.F.ProductVersionFactory(environments=envs)
        cv = self.F.CaseVersionFactory(environments=envs)
        rcv = self.F.RunCaseVersionFactory(
            run__productversion=pv, caseversion=cv)

        pv.remove_envs(envs[0])

        self.assertEqual(set(rcv.environments.all()), set(envs[1:]))


    def test_inherits_env_removal_from_caseversion(self):
        """RCV inherits env removal from caseversion."""
        envs = self.F.EnvironmentFactory.create_full_set(
            {"OS": ["OS X", "Linux"]})
        r = self.F.RunFactory(environments=envs)
        cv = self.F.CaseVersionFactory(environments=envs)
        rcv = self.F.RunCaseVersionFactory(run=r, caseversion=cv)

        cv.remove_envs(envs[0])

        self.assertEqual(set(rcv.environments.all()), set(envs[1:]))


    def test_does_not_inherit_env_addition_to_caseversion(self):
        """RCV does not inherit env added to caseversion."""
        envs = self.F.EnvironmentFactory.create_full_set(
            {"OS": ["OS X", "Linux"]})
        r = self.F.RunFactory(environments=envs)
        cv = self.F.CaseVersionFactory(environments=envs[1:])
        rcv = self.F.RunCaseVersionFactory(run=r, caseversion=cv)

        cv.add_envs(envs[0])

        self.assertEqual(set(rcv.environments.all()), set(envs[1:]))


    def test_result_summary(self):
        """``result_summary`` returns dict summarizing result states."""
        rcv = self.F.RunCaseVersionFactory()

        self.F.ResultFactory(runcaseversion=rcv, status="assigned")
        self.F.ResultFactory(runcaseversion=rcv, status="started")
        self.F.ResultFactory(runcaseversion=rcv, status="passed")
        self.F.ResultFactory(runcaseversion=rcv, status="failed")
        self.F.ResultFactory(runcaseversion=rcv, status="failed")
        self.F.ResultFactory(runcaseversion=rcv, status="invalidated")
        self.F.ResultFactory(runcaseversion=rcv, status="invalidated")
        self.F.ResultFactory(runcaseversion=rcv, status="invalidated")

        self.assertEqual(
            rcv.result_summary(),
            {
                "passed": 1,
                "failed": 2,
                "invalidated": 3,
                }
            )


    def test_result_summary_specific(self):
        """``result_summary`` has results only from one runcaseversion."""
        rcv = self.F.RunCaseVersionFactory()
        self.F.ResultFactory(runcaseversion=rcv, status="passed")

        rcv2 = self.F.RunCaseVersionFactory()

        self.assertEqual(
            rcv2.result_summary(),
            {
                "passed": 0,
                "failed": 0,
                "invalidated": 0,
                }
            )

    def test_result_summary_empty(self):
        """Empty slots in result summary still contain 0."""
        rcv = self.F.RunCaseVersionFactory()

        self.assertEqual(
            rcv.result_summary(),
            {
                "passed": 0,
                "failed": 0,
                "invalidated": 0,
                }
            )


    def test_completion_percentage(self):
        """``completion`` returns fraction of envs completed."""
        envs = self.F.EnvironmentFactory.create_full_set(
            {"OS": ["Windows", "Linux"]})
        rcv = self.F.RunCaseVersionFactory.create(environments=envs)

        self.F.ResultFactory(
            runcaseversion=rcv, environment=envs[0], status="passed")
        self.F.ResultFactory(
            runcaseversion=rcv, environment=envs[0], status="failed")
        self.F.ResultFactory(
            runcaseversion=rcv, environment=envs[1], status="started")

        self.assertEqual(rcv.completion(), 0.5)


    def test_completion_percentage_empty(self):
        """If no envs, ``completion`` returns zero."""
        rcv = self.F.RunCaseVersionFactory.create()

        self.assertEqual(rcv.completion(), 0)


    def test_testers(self):
        """Testers method returns list of distinct testers of this rcv."""
        t1 = self.F.UserFactory.create()
        t2 = self.F.UserFactory.create()
        rcv = self.F.RunCaseVersionFactory.create()
        self.F.ResultFactory.create(tester=t1, runcaseversion=rcv)
        self.F.ResultFactory.create(tester=t1, runcaseversion=rcv)
        self.F.ResultFactory.create(tester=t2, runcaseversion=rcv)

        self.assertEqual(set(rcv.testers()), set([t1, t2]))
