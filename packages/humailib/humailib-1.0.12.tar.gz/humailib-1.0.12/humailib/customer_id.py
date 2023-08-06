import pandas as pd
import warnings
import re

import humailib.utils as hu
import humailib.hasher as hh
from humailib.cloud_tools import GoogleCloudStorage, GoogleBigQuery

class GenerateCustomerID:
    
    def __init__(self):
        self.cid_offset = 0
        
        # email_to_cid:
        # {
        #  'Email' : str(customer_id), 
        #   ...
        # }
        self.email_to_cid = {}

        # Each person can have one or more different email addresses, that need
        # the same Customer_ID
        # person_to_emails=
        # {
        #  'Person' : [email0, email1, ...], 
        #   ...
        # }
        self.person_to_emails = {}
        
        # Each email address could have one or more different persons, for example
        # if a person entered their first name slightly differently in two occasions.
        # emails_to_person=
        # {
        #  'Email' : [person0, person1, ...], 
        #   ...
        # }
        self.email_to_persons = {}
        
    def _walk_emails(self, email, people=[], emails=[]):
        
        for person in self.email_to_persons[email]:
            if person not in people:
                people.append(person)
                for m in self.person_to_emails[person]:
                    if m not in emails:
                        emails.append(m)
                        self._walk_emails(m, people=people, emails=emails)
                
        return people, emails
                
        
    def add(
        self, 
        df, 
        email_col,
        cols_to_match,
        verbose=False
    ):   
        """
        Generate unique Customer IDs for people, based on email address and
        people information from columns.
        
        Each email address gets a unique Customer ID, initially. And then email addresses
        which are different but have matching people information are merged, and get 
        assigned the same Customer ID.
        
        """
        print("[GenerateCustomerID::add] transforming columns...")
        df = df[[email_col]+cols_to_match].copy()
        
        df.loc[:,email_col] = df[email_col].str.strip().str.upper()
        
        def get_person(x, cols_to_match):
            person = [
                re.sub(r'[^\w]', '', x[c]) \
                  .replace('_','') \
                  .upper() for c in cols_to_match
            ]
            if person is None or len(person) == 0:
                return ''
            
            for p in person:
                if p == '':
                    return ''
                
            return '_'.join(person)
        
        # We assume that [cols_to_match] is the minimum information required to
        # uniquely identify and merge a person, so if any of this information is 
        # missing, mark it as an empty person, so it does not get merged.
        df.loc[:,'Person'] = df.apply(lambda x: get_person(x, cols_to_match), axis=1)
        
        for i,email in enumerate(df[email_col].unique()):
            self.email_to_cid[email] = self.email_to_cid.get(email, 'S'+str(i+self.cid_offset))
        
        email_in_common = {}
        
        print("[GenerateCustomerID::add] adding new people to table...")
        
        n_new_people = 0
        n_new_emails = 0
        ii = 0
        nn = len(df)
        for index, row in df.iterrows():

            if ii % 10000 == 0:
                print("  {:,}/{:,} rows ({:.2f}%)".format(
                    ii,
                    nn,
                    100.0*float(ii)/nn
                ))

            person = row['Person']
            
            # Don't attempt to merge empty persons
            if person != '': 
                email = row[email_col]

                if email not in self.email_to_persons:
                    n_new_emails = 1 + n_new_emails
                    self.email_to_persons[ email ] = [ person ]
                elif person not in self.email_to_persons[email]:
                    self.email_to_persons[ email ].append(person)

                if person not in self.person_to_emails:
                    n_new_people = 1 + n_new_people
                    self.person_to_emails[ person ] = [ email ]
                elif email not in self.person_to_emails[person]:
                    self.person_to_emails[ person ].append(email)
                
            ii = 1 + ii
                

        print("[GenerateCustomerID::add] merging ids...")
        n_emails = 0
        n_merged = 0
        nn = len(self.email_to_persons)
        for email in self.email_to_persons.keys():
            # Gather all people and emails that can be 'reached' by shared emails
            people, emails = self._walk_emails(email, people=[], emails=[])
            
            if n_emails % 5000 == 0:
                print("  {:,}/{:,} email addresses ({:.2f}%)".format(
                    n_emails,
                    nn,
                    100.0*float(n_emails)/nn
                ))
            
            #if 'MATERS' in email:
            #    print("------======------")
            #    print(email)
            #    print("walked people: {}".format(people))
            #    print("walked emails: {}".format(emails))
            #    for mm in emails:
            #        print("cid {}".format(self.email_to_cid[mm]))
        
            cid = self.email_to_cid[email]
            # Determine oldest Customer_ID
            for m in emails:
                contestant = self.email_to_cid.get(m,'')
                if contestant != '' and (int(contestant[1:]) < int(cid[1:])):
                    cid = contestant
            
            # Set all these people's emails to oldest Customer_ID
            for m in emails:
                if self.email_to_cid.get(m,'') != cid:
                    n_merged = 1 + n_merged
                    if verbose:# or 'MATERS' in email:
                        print("{} '{}' and '{}' belong to same person: {} (old cid='{}', new cid='{}')".format(
                            n_merged,
                            m,
                            email,
                            self.email_to_persons[m][0],
                            self.email_to_cid[m],
                            cid
                        ))                    
                    self.email_to_cid[m] = cid
                    
            n_emails = 1 + n_emails
            
        cids = [value for _,value in self.email_to_cid.items()]
        
        print("====================")
        print("[GenerateCustomerID::generate_from_transactions] New people: {:,}, new emails {:,}".format(n_new_people, n_new_emails))
        print("[GenerateCustomerID::generate_from_transactions] Unique email addresses with assigned Customer IDs: {:,}, unique Customer IDs {:,}".format(len(self.email_to_cid),len(set(cids))))
        print("[GenerateCustomerID::generate_from_transactions] Total emails in merge-able person table: {:,}, of which merged (but weren't before): {:,}\n".format(n_emails, n_merged))
                
        return self.email_to_cid
    
    
    def get_ids(self, df, email_col='Email'):
    
        """
        """
        return df[email_col].apply(lambda x: self.email_to_cid.get(x.strip().upper(),''))
    
    
    def add_and_get_ids(
        self, 
        df, 
        email_col,
        cols_to_match,
        verbose=False
    ):
        
        """
        """
        self.add(df, email_col=email_col, cols_to_match=cols_to_match, verbose=verbose)
        return self.get_ids(df, email_col)
    
    
    def to_dataframe(self):
        
        """
        """
        if len(self.email_to_cid) == 0 or len(self.person_to_emails) == 0:
            return None
        
        data = []
        for email,cid in self.email_to_cid.items():
            if email in self.email_to_persons:
                for person in self.email_to_persons[email]:
                    data.append((cid, email, person))
            else:
                data.append((cid, email, ''))
                
        df = pd.DataFrame(data, columns=['Customer_ID','Email','Person'])
        hu.columns_as_str(df, columns=['Customer_ID','Email','Person'])

        df.drop_duplicates(inplace=True)
                    
        return df
    
    
    def upload_and_replace(self, dataset_table_name, gbq):
        
        """
        """
        if len(self.email_to_cid) == 0 or len(self.person_to_emails) == 0:
            return False
        
        if gbq is None:
            gbq = GoogleBigQuery()
            
        df = self.to_dataframe()

        hh.encrypt_columns(df, columns=['Email','Person'])
        gbq.upload_and_replace_table(df, dataset_table_name)
        
        return True
        
        
    def load(self, dataset_table_name, gbq, flush_cache=True):
        
        """
        """
        self.__init__()
        
        if gbq is None:
            gbq = GoogleBigQuery()
            
        df_customers = hu.load_table(
            gbq, 
            dataset_table_name, 
            table_type='customer_ids', 
            flush_cache=flush_cache
        )
        if df_customers is None:
            print("[GenerateCustomerID::load] Failed to load customers table '{}'".format(dataset_table_name))
            return False
        
        hh.decrypt_columns(df_customers, columns=['Email','Person'])
        
        self.cid_offset = df_customers.Customer_ID.str[1:].astype(int).max() + 1
        self.email_to_cid = {
            email:cid for (cid,email) in zip(
                df_customers.Customer_ID.to_numpy(),
                df_customers.Email.to_numpy()
            )
        }
        
        self.email_to_persons = {}
        self.person_to_emails = {}
        for index, row in df_customers.iterrows():

            person = row['Person']
            email = row['Email']

            if person != '': 
                                    
                if email not in self.email_to_persons:
                    self.email_to_persons[ email ] = [ person ]
                elif person not in self.email_to_persons[email]:
                    self.email_to_persons[ email ].append(person)

                if person not in self.person_to_emails:
                    self.person_to_emails[ person ] = [ email ]
                elif email not in self.person_to_emails[person]:
                    self.person_to_emails[ person ].append(email)
            
        return True
        
        