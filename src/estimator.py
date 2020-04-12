
def estimator(data):
      currentlyInfectedImpact = int(data['reportedCases'] * 10)
      currentlyInfectedSevereImpact = int(data['reportedCases'] * 50)

      days = timeEstimate(data)

      infectionRequestTimeImpact = currentlyInfectedImpact * (2 ** (int(days / 3)))
      infectionRequestTimeSevereImpact = currentlyInfectedSevereImpact * (2 ** (int(days / 3)))

      severeCaseRequestTimeImpact = (0.15 * infectionRequestTimeImpact)
      severeCaseRequestTimeSevereImpact = (0.15 * infectionRequestTimeSevereImpact)

      beds = (0.35 * int(data['totalHospitalBeds']))

      bedsRequestedTimeImpact = int(beds - severeCaseRequestTimeImpact)
      bedsRequestedTimeSevereImpact = int(beds - severeCaseRequestTimeSevereImpact)

      casesForICUByRequestedTimeImpact = math.floor(0.05 * infectionRequestTimeImpact)
      casesForICUByRequestedTimeSevereImpact = math.floor(0.05 * infectionRequestTimeSevereImpact)

      casesForVentilatorsByRequestedTimeImpact = math.floor(0.02 * infectionRequestTimeImpact)
      casesForVentilatorsByRequestedTimeSevereImpact = math.floor(0.02 * infectionRequestTimeSevereImpact)

      dollarsInFlightImpact = math.floor(infectionRequestTimeImpact * (data['region']['avgDailyIncomePopulation']) * (data['region']['avgDailyIncomeInUSD'])) / days

      dollarsInFlightSevereImpact = math.floor(infectionRequestTimeSevereImpact * (data['region']['avgDailyIncomePopulation']) * (data['region']['avgDailyIncomeInUSD'])) / days



      output = {
        "data":data,
        "impact":{
          "currentlyInfected": currentlyInfectedImpact,
          "infectionsByRequestedTime": currentlyInfectedImpact * (2 ** (int(days / 3))),
          "severeCasesByRequestedTime": severeCaseRequestTimeImpact,
          "hospitalBedsByRequestedTime": bedsRequestedTimeImpact,
          "casesForICUByRequestedTime": casesForICUByRequestedTimeImpact,
          "casesForVentilatorsByRequestedTime": casesForVentilatorsByRequestedTimeImpact,
          "dollarsInFlight": dollarsInFlightImpact
        },
        "severeImpact":{
          "currentlyInfected": currentlyInfectedSevereImpact,
          "infectionsByRequestedTime": currentlyInfectedSevereImpact * (2 ** (int(days / 3))),
          "severeCasesByRequestedTime": severeCaseRequestTimeSevereImpact,
          "hospitalBedsByRequestedTime": bedsRequestedTimeSevereImpact,
          "casesForICUByRequestedTime": casesForICUByRequestedTimeSevereImpact,
          "casesForVentilatorsByRequestedTime": casesForVentilatorsByRequestedTimeSevereImpact,
          "dollarsInFlight": dollarsInFlightSevereImpact

        }
        
      }

      return output


def timeEstimate(data):
      if data['periodType'] == 'days':
              days = data['timeToElapse']

      elif data['periodType'] == 'weeks':
              days = data['timeToElapse'] * 7

      elif data['periodType'] == 'months':
              days = data['timeToElapse'] * 30
      return days
