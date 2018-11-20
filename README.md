This is a short python project that keeps track of attendance of a group of 
people over time. A person that attends an event receives a point, while a 
person that misses the event without an excuse is issued a strike.

The script, when executed, reads through an existing CSV file of points and 
strikes. Then, the script asks for a CSV file with the actual attendance at an
event, a CSV file with the expected attendance for that event, and the name of 
the event.

The script then compares the expected and actual attendance files, modifies the
existing attendance tracker CSV with the new points and strikes for each person
and also sends an email notification to each person that received a strike for
that event with a count of their overall strikes as well. 