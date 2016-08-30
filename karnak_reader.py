import urllib
from operator import itemgetter
from datetime import date
from HTMLParser import HTMLParser


res_to_karnak_map = { 'stampede'    : 'stampede.tacc.xsede.org',
                      'gordon'      : 'gordon.sdsc.xsede.org',
                      'comet'       : 'comet.sdsc.xsede.org'
                    }

class karnakParser(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.output = list()
        self.karnak_list = list()

    def handle_data(self, data):
        if data != '\n':
            self.output.append(data)

    def clean_data(self):
        if self.output[0] == "Job is unknown on specified system\n":
            print "Job doesn't exist"
        else:
            print self.output[0]
            job = self.output[0].split()
            self.karnak_list.append((job[0] + "_ID", job[1]))
            self.karnak_list.append(('Resource', job[3]))
            
            cur_year = str(date.today().year)
            self.karnak_list.append(("Submit_Date", self.output[7].split(' ')[0] + "/" + cur_year))
            self.karnak_list.append(("Submit_Time_(CDT)", self.output[7].split(' ')[1]))
            self.karnak_list.append(("Processors", int(self.output[8])))
            self.karnak_list.append(("Requested_Wall_Time", self.output[9]))
            self.karnak_list.append(("Predicted_Wait_Time", self.output[10].split('\n')[0]))
            self.karnak_list.append(("90%_Confidence_Interval", self.output[11][2:]))
            self.karnak_list = sorted(self.karnak_list, key=itemgetter(0))
            return self.karnak_list


def job_id_parse(resource, saga_id):
    
    job_id = ""
    if resource == 'stampede':
        job_id = saga_id.split('-')[1].split(']')[0].split('[')[1]
        return job_id

def karnak_query(resource, saga_id):

    job_id = job_id_parse(resource, saga_id)
    link = 'http://karnak.xsede.org/karnak/system/' + res_to_karnak_map[resource] + '/job/' + job_id + '/prediction/waittime.html'
    l = urllib.urlopen(link)
    mylink = l.read()

    parser = karnakParser()
    parser.feed(mylink)

    return parser.clean_data()



if __name__ == "__main__":
    
    stampede_parse = '[slurm+ssh://tg829619@stampede.tacc.utexas.edu]-[7559642]'
    #job_id_parse('stampede', stampede_parse) 
    #link = "http://karnak.xsede.org/karnak/system/stampede.tacc.xsede.org/job/7559279/prediction/waittime.html"
    karnak_query('stampede', stampede_parse)
