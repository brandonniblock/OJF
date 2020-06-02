import OJF as OJF

def main():
    ojf = OJF.OJF()

    company_list = ojf.getListOfCompanies()
    #ojf.findIfJobsAreOpen()
    ojf.createFile() #contains a list of companies with a recent job opening
    ojf.sendEmail() #sends me an email if they company has a job opening 

main()