import scrapy
import urllib
from scrapy.http import FormRequest
import logging
import os
import time
import requests
from os.path import expanduser
from PMGSY.config import URL
from PMGSY.data_dumpers import PMGSYDataDumper
from PMGSY.scrapers.PMGSY_Scraper import PMGSYScraper

class PMGSYSpider(scrapy.Spider):
    name = "PMGSY_Spider_District"
    start_urls = [URL]

    def __init__(self, data_dir_path=expanduser('~/PMGSY/PMGSY_Spider'), *args, **kwargs):
        self.data_dir_path = data_dir_path
        if not os.path.isdir(self.data_dir_path):
            os.makedirs(self.data_dir_path)
        super(PMGSYSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        print "district one running"
        PMGSYDataDumper(self.data_dir_path).createHeading()        
        states = self.getStates(response)
        months = self.getMonths(response)
        years = self.getYears(response,2013)
        baseUrl = 'http://omms.nic.in/MvcReportViewer.aspx?'
        params = {}
        params['_r']='/PMGSYCitizen/MPR1_Dynamic'
        params['AGENCY']='0'
        params['AgencyName']='All+Agencies'
        params['Block']='0'
        params['BlockName']='0'
        params['Collaboration']='0'
        params['CollaborationName']='0'
        params['Level']='2'
        params['LocalizationValue']='en'
        params['pDisplayFields']=Helper().getDisplayFields()
        params['PMGSY']='0'
        for year in years:
            for month in months:
                for state in states:
                    districts = self.getDistricts(state['value'])
                    for district in districts:
                        time.sleep(10)
                        params['Month'] = month['value']
                        params['MonthName']=month['displayName']
                        # params['State']=state['value']
                        # params['StateName']=state['displayName'].replace(' ','+')
                        params['State']=2
                        params['StateName']='Andhra+Pradesh'
                        params['DistName']=district['Text'].strip().replace(' ','+')
                        params['District']=district['Value']
                        params['Year']=year['value']
                        params['YearName']=year['displayName']
                        PMGSYMeta = {
                        "stateName":state['displayName'],
                        "year": year['displayName'],
                        "month": month['displayName'],
                        "districtName": district['Text'].strip()
                        }
                        url = baseUrl+urllib.urlencode(params).replace('%2C',',').replace('%2B','+').replace('%2F','/')
                        yield FormRequest(url=url,callback=self.middlewareDistrict,errback=self.error,meta=PMGSYMeta)
                break
            break
       

    def middlewareDistrict(self,response):
    	data = {}
        data['__ASYNCPOST']='true'
        data['__EVENTTARGET']='ReportViewer$ctl09$Reserved_AsyncLoadTarget'
        data['ctl02'] = 'ctl02|ReportViewer$ctl09$Reserved_AsyncLoadTarget'
        data['ReportViewer$AsyncWait$HiddenCancelField']='False'
        data['ReportViewer$ctl07$collapse']='false'
        data['ReportViewer$ctl09$ReportControl$ctl04']='100'
        data['ReportViewer$ctl09$VisibilityState$ctl00']='None'
        yield FormRequest.from_response(
                      response, formdata = data, callback = self.PMGSYDistrict,
                      errback = self.error, meta=response.meta
                      )
    def PMGSYDistrict(self,response):
        rows=response.css('tr')
        usefulRows = rows[13:-4]
        if len(usefulRows) == 0:
            logging.critical('No Data Found '+response.meta['stateName']+' '+response.meta['districtName']+' '+response.meta['month']+' '+response.meta['year'])
            return
        for i in range(0,len(usefulRows)/2):
            districtName = PMGSYScraper().getDistrictName(usefulRows[2*i])
            if districtName == response.meta['districtName']:
                districtData = PMGSYScraper().getDistrictData(usefulRows[2*i+1])
                PMGSYDataDumper(self.data_dir_path).dump(response.meta['year'],response.meta['month'],\
                    response.meta['stateName'],districtName, districtData)


    def error(self):
    	logging.critical('Request Failed')

    def getStates(self, response):
    	stateOptions = response.xpath('//*[(@id = "StateList_CompletedRoadDetails")]').css('option')[1:]
        states = []
        for state in stateOptions:
            displayName = state.css('::text').extract_first().strip()
            value = state.css('::attr(value)').extract_first().strip()
            states.append(Helper().makeResponse(displayName,value))
        return states

    def getMonths(self, response):
    	monthOptions = response.xpath('//*[(@id = "ddlMonthMPR1")]').css('option')
    	months = []
    	for month in monthOptions:
    		months.append(Helper().makeResponse(month.css('::text').extract_first(),month.css('::attr(value)').extract_first()))
    	return months

    def getYears(self, response, minYear):
    	yearOptions = response.xpath('//*[(@id = "ddlYearMPR1")]').css('option')
    	years = []
    	for year in yearOptions:
    		yearValue = year.css('::attr(value)').extract_first()
    		yearDisplay = year.css('::text').extract_first()
    		years.append(Helper().makeResponse(yearDisplay,yearValue))
    	return years

    def getDistricts(self,StateCode):
        districtURL='http://omms.nic.in/ProposalArea/Proposal/DistrictDetails'
        r = requests.post(districtURL, data={"StateCode":StateCode})
        return r.json()[1:]


class Helper():
	def makeResponse(self, displayName, value):
		return {
		"displayName": displayName,
		"value": value
		}

	def getDisplayFields(self):
		ans = ''
		for i in range(1,43):
			if i < 10:
				ans+='0'
			ans+=str(i)+','
		return ans[:-1]