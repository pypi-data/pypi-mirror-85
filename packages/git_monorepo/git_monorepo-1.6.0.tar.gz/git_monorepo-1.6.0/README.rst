Monorepo support built around ``git subtree``.

Installation
============

.. code:: sh

    pip install git_monorepo

Usage
=====

Simply create a mapping file called ``monorepo.yml`` in the root of your
git directory:

.. code:: yaml

    mappings:
      adhesive: git@github.com:germaniumhq/adhesive.git
      oaas:
        oaas: git@github.com:germaniumhq/oaas.git
        grpc-compiler: git@github.com:germaniumhq/oaas-grpc-compiler.git
        registry-api: git@github.com:germaniumhq/oaas-registry-api.git
        registry: git@github.com:germaniumhq/oaas-registry.git
        grpc: git@github.com:germaniumhq/oaas-grpc.git
        simple: git@github.com:germaniumhq/oaas-simple.git
      tools:
        git-monorepo: git@github.com:bmustiata/git-monorepo.git

pull
----

To pull the repos (including initial setup), use:

.. code:: sh

    git mono pull

In case upstream changes happened in the remote repos, so a pull is
required before the push, use the ``--no-sync`` flag, so it won’t
automatically merge and mark the changes as already synchronized to the
remote repo.

Implicity having a ``pull`` should be done on a clean repo, and a ``pull
--no-sync`` if upstream changes are present.

push
----

To push the repos do:

.. code:: sh

    git mono push

This takes into account the current branch name, so pushes can happen
also with branches.

At the end of the operation, if something was pushed, a new file to
track the status named ``.monorepo.sync`` is created and committed
automatically. This file holds a list of commits that were pushed, so
your merges can also be dealed with correctly, by adding both entries
when solving a potential conflict for a project.

mv
--

This renames the entry in the synchronized commits, and does the
equivalent of:

.. code:: sh

    git mv old/path new/path
    git subtree split --rejoin --prefix=new/path HEAD
    git subtree pull --squash --prefix=new/path giturl branch

WARN: You still need to manually update the ``monorepo.yml`` manually
with the new location.
