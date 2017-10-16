	from __future__ import division
	import numpy as np
	from matplotlib import pyplot as plt
	import glob
	import csv
	
	def calcJ( matrix, hour1, day1, theta0, theta1, theta2 ):
	   J = 0;
	   for i in xrange(24):
	    for j in xrange(31):
	        
	        J = J + ((theta0*hour1[i] + theta1*day1[j] + theta2) - matrix[i][j]) * ((theta0*hour1[i] + theta1 * day1[j] + theta2) - matrix[i][j]);
	        #print image_list[i],distance[i],J,theta0,theta1
	   J = 0.125 * J;  
	   #print J
	   return J
	
	
	
	#for filename in glob.glob('[0-9]*ft.jpg'): #assuming gif
	ifile  = open('data.csv', "rb")
	reader = csv.reader(ifile)
	
	rownum = 0
	
	w, h = 31 , 24
	matrix = [[0 for x in range(w)] for y in range(h)] 
	
	frequency = [0 for y in range(h)]
	hour1 = [0.0, 0.043478260869565216, 0.08695652173913043, 0.13043478260869565, 0.17391304347826086, 0.21739130434782608, 0.2608695652173913, 0.30434782608695654, 0.34782608695652173,0.391304347826087,0.43478260869565216, 0.4782608695652174, 0.5217391304347826, 0.5652173913043478, 0.6086956521739131, 0.6521739130434783, 0.6956521739130435, 0.7391304347826086, 0.782608695652174, 0.8260869565217391, 0.8695652173913043, 0.9130434782608695, 0.9565217391304348, 1.0]
	day1 = [0.03225806451612903, 0.06451612903225806, 0.0967741935483871, 0.12903225806451613, 0.16129032258064516, 0.1935483870967742, 0.22580645161290322, 0.25806451612903225, 0.2903225806451613, 0.3225806451612903, 0.3548387096774194, 0.3870967741935484, 0.41935483870967744, 0.45161290322580644, 0.4838709677419355, 0.5161290322580645, 0.5483870967741935, 0.5806451612903226, 0.6129032258064516, 0.6451612903225806, 0.6774193548387096, 0.7096774193548387, 0.7419354838709677, 0.7741935483870968, 0.8064516129032258, 0.8387096774193549, 0.8709677419354839, 0.9032258064516129, 0.9354838709677419, 0.967741935483871, 1.0]
	
	
	for row in reader:
	    
	        
	    if rownum == 0:
	        header = row
	        summ = 0
	        day = 0
	        hour = 0
	    else:
	        colnum = 0
	        for col in row:
	            if colnum % 4 == 3:
	            summ += int( col)
	
	        colnum += 1
	           
	    if rownum % 60 == 1:        
	        #print '%s %-8s: %f %d' % (row[0],header[1],summ /60.0 ,rownum)
	        matrix[hour][day] = summ / 60.0
	        if hour == 9 and day == 0:
	            print hour,day
	            print matrix[hour][day]
	            print '%s %-8s: %f %d' % (row[0],header[1],summ /60.0 ,rownum)
	        summ = 0  
	        hour += 1
	        if hour % 24 == 0:
	           hour = 0
	           day += 1
	
	    rownum += 1     
	    
	ifile.close()
	
	for x in range(w):
	    for y in range(h):
	        if matrix[y][x] > 15:
	            frequency[y] += 1
	
	
	print frequency
	
	#theta0 = 9
	#theta1 = -1/30
	
	theta0 = 1
	theta1 = 0
	theta2 = 1
	
	Jold = 0
	Jnew = -10
	diff_J0 = 0
	diff_J1 = 0
	diff_J2 = 0
	counter = 0
	
	while ((Jold - Jnew > 0.00000000000001) or (Jnew - Jold > 0.00000000000001)):
	    diff_J0 = 0;
	    diff_J1 = 0;
	    diff_J2 = 0;
	    for i in xrange(24):
	        for j in xrange(31):
	            temptheta = 1 * ((theta0*hour1[i] + theta1*day1[j] + theta2) - matrix[i][j]) ;  
	            diff_J0 = diff_J0 + 1 * hour1[i] * ((theta0*hour1[i] + theta1*day1[j] + theta2) - matrix[i][j]) / 720.0;
	            
	
	    temp0 = theta0 - diff_J0;
	    
	    diff_J1 = 0
	    for i in xrange(24):
	        for j in xrange(31):
	            temptheta = 1 * ((theta0*hour1[i] + theta1*day1[j] + theta2) - matrix[i][j]) / 720.0;   
	            diff_J1 = diff_J1 + 1 * day1[j] * ((theta0*hour1[i] + theta1*day1[j] + theta2) - matrix[i][j]) / 720.0;
	            
	        
	    temp1 = theta1 - diff_J1;
	    
	    diff_J2 = 0
	    for i in xrange(24):
	        for j in xrange(31):
	            temptheta = 1 * ((theta0*hour1[i] + theta1*day1[j] + theta2) - matrix[i][j]) / 720.0;   
	            diff_J2 = diff_J2 + 1 * ((theta0*hour1[i] + theta1*day1[j] + theta2) - matrix[i][j]) / 720.0;
	            
	
	    temp2 = theta2 - diff_J2;
	    
	    theta0 = temp0
	    theta1 = temp1
	    theta2 = temp2
	    counter = counter + 1;
	    Jold = Jnew
	    #print Jold
	    #print Jnew
	    Jnew = calcJ(matrix,hour1,day1,theta0,theta1,theta2)
	    counter += 1;
	
	print theta0,theta1,theta2
	#print Jold,Jnew 
	print counter   
	
	
	print matrix[10][0]
