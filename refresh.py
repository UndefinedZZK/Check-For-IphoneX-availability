import sched, time, logging, requests
import os
colorToPartNumber = {'white': 'MQAG2B/A', 'black': 'MQAF2B/A'}
yourAddress = 'WC1E 6BT'

def getAddressForURL():
	return yourAddress.replace(' ', '%20')

def notify(title, subtitle, message):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    os.system('terminal-notifier {}'.format(' '.join([m, t, s])))

def checkPickupInStoreList(storeList, color):	
    for store in storeList:
    	pickupSituationForStores = store['partsAvailability'][colorToPartNumber[color]]['storePickupQuote']
    	print ' '.join([time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime()), 'iPhone 256G with color', color, pickupSituationForStores])
    	pickupSituationAbbreviation = store['partsAvailability'][colorToPartNumber[color]]['pickupSearchQuote']
    	if (pickupSituationAbbreviation != 'Currently unavailable'):
    		notifyMessage = str(' '.join(['Iphone X with color', color, pickupSituationForStores]))
    		notify('Buy your ipx now!!!', 'From Python script created by UndefinedZZK', notifyMessage)
    		return

def scheduleCheckPerSeconds(scheduler, interval): 
	requestURLforWhite = ''.join(['https://www.apple.com/uk/shop/retail/pickup-message?pl=true&parts.0=', colorToPartNumber['white'], '&location=', getAddressForURL()])
	requestURLforBlack = ''.join(['https://www.apple.com/uk/shop/retail/pickup-message?pl=true&parts.0=', colorToPartNumber['black'], '&location=', getAddressForURL()])
	storeListforWhite = requests.get(requestURLforWhite).json()['body']['stores']
	storeListforBlack = requests.get(requestURLforBlack).json()['body']['stores']
	checkPickupInStoreList(storeListforWhite, 'white')
	checkPickupInStoreList(storeListforBlack, 'black')
	scheduler.enter(interval, 1, scheduleCheckPerSeconds, (scheduler, interval, ))
	print '==================================================================================================='

print "Start looking for availbility"
ipxAvailabilityScheduler = sched.scheduler(time.time, time.sleep)
ipxAvailabilityScheduler.enter(0, 1, scheduleCheckPerSeconds, (ipxAvailabilityScheduler, 15, ))
ipxAvailabilityScheduler.run()