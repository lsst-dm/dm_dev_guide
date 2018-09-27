#!/usr/bin/env python

#
# This file is part of ...
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""Copyright file generator.

This script runs "git log" to determine the authors of commits to a repository
or set of paths within a repository and then generates a COPYRIGHT file
corresponding to those authors and the dates of their commits.
"""


import collections
import os
import re
import subprocess
import sys

INSTITUTIONS = {
        "Association of Universities for Research in Astronomy":
            ["noao.edu", "lsst.org", "LSST.org", "simon.krughoff@gmail.com",
                "wmwv@pitt.edu", "josh@hoblitt.com", "womullan@sciops.esa.int",
                "womullan@users.noreply.github.com", "jonathansick@mac.com",
                "jmatt@jmatt.org", "athornton@gmail.com"],
        "California Institute of Technology":
            ["caltech.edu"],
        "The Board of Trustees of the Leland Stanford Junior "
            "University, through SLAC National Accelerator Laboratory":
            ["slac.stanford.edu", "vaikunth@tamu.edu",
                "jgates@slac.standford.edu", # !!!
                "fabrice.jammes@in2p3.fr",
                "fabrice.jammes@clermont.in2p3.fr",
                "aaoualid@gmail.com", "abh@stanford.edu", "astro@mandeep.org"],
        "The Regents of the University of California":
            ["ucdavis.edu",
                "pgee@physics.ucdavis.com", # !!!
                "pgee@pgeepc2.gateway.2wire.net"],
        "The Trustees of Princeton University":
            ["princeton.edu", "rearmstr@gmail.com",
                "vishal.kasliwal@gmail.com", "merlin.fisherlevine@gmail.com",
                "jmeyers314@gmail.com"],
        "The University of Tokyo":
            ["steven.bickerton@gmail.com"],
        "University of Illinois Board of Trustees":
            ["illinois.edu", "daues@users.noreply.github.com"],
        "University of Washington":
            ["uw.edu", "washington.edu", "ctslater@umich.edu",
                "ianssullivan@gmail.com", "scott.f.daniel@gmail.com",
                "John.Parejko@alumni.carleton.edu"]
}
"""Dictionary of institutions claiming copyright.

Key is the official copyright text for the institution.  Value is a list of
suffixes for emails belonging to that institution.
"""

THRESHOLD = 3
"""Significance threshold for copyright, in number of lines.

A commit is deemed significant for copyright purposes if it
adds, deletes, or changes at least this number of lines.
"""

def find_institution(email, year, month):
    """Find the institution for an author's email on a given date.

    All code was assigned to LSST Corporation prior to the start of
    construction in 2014-08.

    John Swinbank moved from Princeton to UW at the end of 2017-09.

    Parameters
    ----------
    email : `str`
        Email of the commit author (not committer).
    year : `int`
        Year that the commit was made.
    month : `int`
        Month that the commit was made.

    Returns
    -------
    institution : `str`
        Copyright text for the institution which claims copyright to the
        author's work, or the author's email if no institution.
    """
    if year < 2014 or (year == 2014 and month < 8):
        return "LSST Corporation"
    if email == "swinbank@lsst.org":
        if year < 2017 or (year == 2017 and month < 10):
            return "The Trustees of Princeton University"
        return "University of Washington"
    for institution in INSTITUTIONS:
        for domain in INSTITUTIONS[institution]:
            if email.endswith(domain):
                return institution
    return email

def format_year_range(min_year, max_year):
    """Format a range of years into a string.

    Parameters
    ----------
    min_year : `intr`
        Low end of the range (inclusive).
    max_year : `intr`
        High end of the range (inclusive).

    Returns
    -------
    text : `str`
        Formatted year range.
    """
    if min_year == max_year:
        return str(min_year)
    else:
        return "%d-%d" % (min_year, max_year)

def stringify_year_set(years):
    """Convert a set of years into a list of year ranges.

    Parameters
    ----------
    years : `set` of `int`
        Set of years.

    Returns
    -------
    text : `str`
        Formatted year range list.
    """
    year_list = sorted(years)
    min_year = max_year = year_list[0]
    year_ranges = []
    for year in year_list[1:]:
        if year == max_year + 1:
            max_year = year
        else:
            year_ranges.append(format_year_range(min_year, max_year))
            min_year = max_year = year
    year_ranges.append(format_year_range(min_year, max_year))
    return ", ".join(year_ranges)


if __name__ == "__main__":
    # Log format includes the author date in ISO-like format, author email,
    # and full commit hash.
    git_cmd = ["git", "log", "--pretty=format:%ai %ae %H", "--shortstat"]

    # Append any other git arguments from the command line.
    if len(sys.argv) > 1:
        git_cmd += sys.argv[1:]

    log = subprocess.check_output(git_cmd, universal_newlines=True)

    # Read in the full hashes of any commits deemed not copyrightable.
    insignificant_list = []
    if os.path.isfile(".non-copyright"):
        with open(".non-copyright", "r") as f:
            for line in f:
                # Allow for comments by only taking hashes at the beginning of
                # a line.  Text that follows the hash or appears on lines that
                # don't begin with a hex character is ignored.
                m = re.search(r"^([\da-f]{40})", line)
                if m:
                    insignificant_list.append(m.group(1))

    copyrights = collections.defaultdict(set)

    for line in log.split("\n"):
        # One pretty-formatted line per commit.
        m = re.search(
                r"^(\d{4})-(\d\d)-\d\d [\d:]+ [+-]\d{4} (\S+) ([\da-f]+)$",
                line)
        if m:
            year = int(m.group(1))
            month = int(m.group(2))
            email = m.group(3)
            commit_hash = m.group(4)
        else:
            # One (or zero, e.g. for merges) shortstat line per commit.
            m = re.search(r"^ \d+ file.+?, (\d+) .+?(?:, (\d+) del.*)?$", line)
            if m:
                # Test for commit significance.
                if int(m.group(1)) >= THRESHOLD or (
                        m.group(2) is not None and
                        int(m.group(2)) >= THRESHOLD):
                    if commit_hash not in insignificant_list:
                        institution = find_institution(email, year, month)
                        copyrights[institution].add(year)

    for institution in copyrights:
        print("Copyright {} {}".format(
            stringify_year_set(copyrights[institution]), institution))
