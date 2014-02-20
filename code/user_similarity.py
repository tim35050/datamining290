from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol

class UserSimilarity(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol

    ###
    # TODO: write the functions needed to
    # 1) find potential matches, 
    # 2) calculate the Jaccard between users, with a user defined as a set of
    # reviewed businesses
    ##/

    def select_user_business(self, _, record):
        """Take in a record, filter by type=review, yield <user_id, business_id>"""
        if record['type'] == 'review':
            yield [ record['user_id'] , record['business_id'] ]

    def select_user_businesses(self, user_id, business_ids):
        """Return what you get """
        bset = set(business_ids)
        yield [ user_id, list(bset) ]
    
    def aggregate_user_businesses(self, user_id, unique_business_ids):
        """Filter out repeat business reviews and return business set """
        yield [ "ALL", [ user_id, list(unique_business_ids) ] ]

    def calculate_jaccard(self, stat, user_business_ids):
        user_business_list = list(user_business_ids)
        for i in range(len(user_business_list)-1):
            for j in range(i + 1, len(user_business_list)):
                user1 = user_business_list[i]
                user2 = user_business_list[j]
                u1set = set(user1[1])
                u2set = set(user2[1])
                jaccard = len(u1set.intersection(u2set)) / float(len(u1set.union(u2set)))
                if jaccard > 0.5:
                    yield [ [user1[0], user2[0] ], jaccard] 

    def select_results(self, stat, answer):
        yield [stat, answer]

    def steps(self):
        """TODO: Document what you expect each mapper and reducer to produce:
        select_user_business: <line, record> => <user_id, business_id>
        select_user_businesses: <user_id, [business_id]> => <user_id, [unique_business_id]>
        aggregate_user_businesses: <user_id, [unique_business_id]> => <"ALL", [user_id,[unique_business_id]]>
        calculate_jaccard: <"ALL",[user_id,[unique_business_id]]> => <[user1,user2],jaccard>
        """
        return [self.mr(mapper=self.select_user_business, reducer=self.select_user_businesses),
                self.mr(mapper=self.aggregate_user_businesses, reducer=self.calculate_jaccard)]
                

if __name__ == '__main__':
    UserSimilarity.run()
