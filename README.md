# RealtimeKafka_EngagementDashboard
I create steam near realtime using kafka (confulence) by run on Ubvuntu in AWS and flow below :

# Flow overview
![image](https://github.com/user-attachments/assets/f6909ca8-d041-4744-ae2a-babfcc528acb)



# Flow in kafka (confluence)

![image](https://github.com/user-attachments/assets/d0b141e3-b1a5-4bb7-930f-a66da4c499f4)


# docker-compose.yml what is about service
Broker   -- kafka name first
broker1 -- kafka of second
broker2 -- kafka of third
schema-registry – support control format schema type data Json,Avro …  from topic.
Connect – using connection other source or data generation for mock data
ksqldb-server – control server backend of kqldb.
ksqldb-cl  -- UI interphase write code sql script and flow.
rest-proxy –  support broker fail or down.
control-center  -- UI Interphase of kaka (confluent)
pinot-zookeeper – The central brain for coordination.
pinot-broker  --  Manages queries and delivers results to users.
pinot-server -- Stores actual data and executes queries.


#  topic
Topic 1 : users_engagement
Topic 2 : users_
Topic 3 : pageviews_
Topic 4 : users_engagement_clean_T4
Topic 5 : users_engagement_joinAgg_T5
Topic 6 : ACTION_TUMLING_T6
Topic 7 : DEVICE_HOPPING_T7
Topic 8 : COUNTRY_WINDOW_T8

# table
users_engagement
users_
pageviews_
users_engagement_clean_T4
users_engagement_joinAgg_T5
ACTION_TUMLING_T6
DEVICE_HOPPING_T7
COUNTRY_WINDOW_T8


##kaka##confluenct ##steaming ##python ##pinot ##Steamlit
