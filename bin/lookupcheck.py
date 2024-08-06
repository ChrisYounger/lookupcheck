# Copyright (C) 2024 Chris Younger

import os, csv
import splunk.Intersplunk

def lookupcheck():

    results, dummyresults, settings = splunk.Intersplunk.getOrganizedResults()
    
    if len(results) == 0:
        results = [{"lookupcheck_status": "ERROR provide a list of CSV file full paths in the \"path\" field"}]
    else:
        problem_limit = 10
        for row in results:
            problems = []
            if not "path" in row:
                problems.append("ERROR path field not found")
            elif row["path"] == "":
                problems.append("ERROR path field is blank")
            else:
                if not os.path.isfile(row["path"]):
                    problems.append("ERROR file not found")
                else:
                    size = -1
                    try:
                        size = os.path.getsize(row["path"])
                    except OSError:
                        pass                
                    row["lookupcheck_size"] = str(size)
                    if not row["path"].lower().endswith('.csv'):
                        problems.append(f"WARN no csv extension on file")
                    with open(row["path"]) as csv_file:
                        try:
                            csv_reader = csv.reader(csv_file, delimiter=',')
                            line_count = 0
                            expected_column_count = 0
                            for csvrow in csv_reader:
                                line_count += 1
                                column_count = len(csvrow)
                                if line_count == 1:
                                    expected_column_count = column_count
                                    # not outputting the row becuase this doesnt correctly do csv escaping
                                    #row["lookupcheck_columns"] = ",".join(csvrow)
                                    for column in csvrow:
                                        column_trimmed = column.strip()
                                        if column_trimmed == "":
                                            problems.append(f"WARN blank column header field")
                                        elif column_trimmed != column:
                                            problems.append(f"ERROR column \"{column_trimmed}\" has leading or trailing whitespace")
                                else:
                                    if expected_column_count != column_count:
                                        problems.append(f"ERROR line {line_count} expected {expected_column_count} column/s found {column_count}")
                                
                        except Exception as ex:
                            problems.append("ERROR unexpected exception: " + str(ex))
            problem_count = len(problems)
            if problem_count > problem_limit:
                row["lookupcheck_status"] = "\n".join(problems[:(problem_limit-1)]) + f"\nNot showing {problem_count-problem_limit+1} more problems..."
            elif problem_count:
                row["lookupcheck_status"] = "\n".join(problems)
            else:
                row["lookupcheck_status"] = "OK"
            
    splunk.Intersplunk.outputResults(results)

if __name__ == '__main__':
    lookupcheck()
