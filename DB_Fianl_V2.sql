-- ################################################################################
-- Question 1
-- Add/Update info for an employee
UPDATE `feitian`.`Employee` SET `Hourly_Rate` = '$40' WHERE (`SSN` = '724390275');
INSERT INTO `feitian`.`Employee` (`SSN`, `Start_Date`, `Hourly_Rate`) VALUES ('724390276', '2010/10/10', '$50');

-- Delete info for an employee 
DELETE FROM `feitian`.`Employee` WHERE (`SSN` = '724390275');

-- Add/Update info for an customer
INSERT INTO `feitian`.`Customer` (`SSN`, `Email_Address`, `Credit_Card#`, `Account#`, `Preference`) VALUES ('724390120', 'kevins@gmail.com', '214741239', '10006', 'None');
UPDATE `feitian`.`Customer` SET `Preference` = 'Next to Window' WHERE (`Credit_Card#` = '2147483221');

-- Delete info for an customer 
DELETE FROM `feitian`.`Customer` WHERE (`Credit_Card#` = '2147483647');


-- ################################################################################
-- Question 2
-- obtain a sales report for a particular month (October)
SELECT *
FROM Reservation 
WHERE DATE(Reserved_Date) BETWEEN '2022-10-01' AND '2022-10-31'
-- WHERE DATE(Reserved_Date) BETWEEN '2022-05-01' AND '2022-05-30'


-- ################################################################################
-- Question 3
-- Produce comprehensive listing of all flights
select *
from Flights


-- ################################################################################
-- Question 4
-- Produce a list of reservations by flight number or by customer name
SELECT *
FROM Reservation 
WHERE `Account#` = 10002 OR `Flight#` = 'Boeing_00735'

SELECT *
FROM Reservation 
WHERE `Account#` = 10002

SELECT *
FROM Reservation 
WHERE `Flight#` = 'Boeing_00735'


-- ################################################################################
-- Question 5
-- Produce a summary listing of revenue generated by a particular flight#
select `Flight#`, sum(TotalFare)
from Reservation 
group by `Flight#`

-- Produce a summary listing of revenue generated by a particular customer#
select Account_Num, sum(TotalFare)
from Reservation 
where Account_Num = '10002'

-- Produce a summary listing of revenue generated by a particular destination city#
select `Flight#`, sum(TotalFare)
from Flights F
where F.Destination-City = 
group by `Flight#`

-- ################################################################################
-- Question 6
-- Determine which customer generated most total revenue
select First_Name, Last_Name, Account_Num, sum_totafare 
from
(select SSN, Account_Num, sum_totafare
from
(select *
from
(select Account_Num, sum(TotalFare) as sum_totafare
from Reservation 
group by Account_Num 
order by sum(TotalFare) desc
limit 1) as tmp , Customer c
where c.`Account#` = tmp.Account_Num) as tmp1) as tmp2, People p
where tmp2.SSN = p.SSN

-- ################################################################################
-- Question 7
-- Most Active Flight
select `Flight#`, Days_of_Week
from Flights 
group by `Flight#`
order by char_length(Days_of_Week) desc
limit 1


-- ################################################################################
-- Question 8
-- List of all customers who have seats reserved on a given flight
select c.`Account#`, p.First_Name, p.Last_Name, r.`Flight#`
from Reservation r, Customer c, People p
where `Flight#` = 'HI_002' AND r.Account_Num = c.`Account#` AND c.SSN = p.SSN


-- ################################################################################
-- Question 9
select f.`Flight#`, s.AirportID, f.Flight_Fare, f.`Destination-City`
from Stops s, Flights f
where s.AirportID = 'HNL' AND s.`Flight#` = f.`Flight#`



-- ################################################################################
-- Question 10
UPDATE `feitian`.`Customer` SET `Preference` = 'Meat' WHERE (`Credit_Card#` = '2147483221');


-- ################################################################################
-- Get all flights for going to an Airport in a City
-- Going to Honolulu
select AirlineID, fl.`Flight#`, Flight_Fare, Stops, Number_of_Seats, Days_of_Week
from Flights fl
inner join Stops st on fl.`Flight#` = st.`Flight#` 
inner join Airport ar on st.AirportID = ar.AirportID
where ar.City = 'Honolulu'
-- Going to London
-- where ar.City = 'London'

-- ################################################################################
-- Customer
-- ################################################################################
-- ################################################################################
-- Question11
-- ################################################################################

-- Question11
-- ################################################################################
-- Question11
-- ################################################################################
-- Question11
-- ################################################################################
-- Question11
-- ################################################################################
-- Question19
            SELECT *
            FROM Reservation 
            WHERE `Account_Num`  = %s
-- ################################################################################









select AirlineID, fl.`Flight#`, Flight_Fare, Stops, Number_of_Seats, Days_of_Week
from Flights fl
inner join Stops st on fl.`Flight#` = st.`Flight#` 
inner join Airport ar on st.AirportID = ar.AirportID
where ar.City = 'Honolulu'

select `Flight#`
from Flights f1  ,Reservation r1
where f1.'Destination-City' = Honolulu and f1'Flight#' = r1'Flight#'
group by `Flight#`