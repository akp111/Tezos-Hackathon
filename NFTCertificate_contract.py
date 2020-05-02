import smartpy as sp

class TezNFT(sp.Contract):
    def __init__(self, _name, _symbol, _admin):
        self.init(
            name = _name,
            
            symbol = _symbol,
            
            admin = _admin,
            
            tokensMinted = sp.set( t= sp.TString),
            
            tokenHolderToID = sp.big_map(tkey = sp.TAddress, tvalue = sp.TSet(sp.TString)),
            
            ownerToBalance = sp.big_map(tkey = sp.TAddress, tvalue = sp.TInt),
            
            tokenIdToOwner = sp.big_map(tkey = sp.TString, tvalue = sp.TAddress),
            
            addressToName = sp.big_map(tkey = sp.TAddress, tvalue = sp.TString),
           
            tokenIDToScore = sp.big_map(tkey = sp.TString, tvalue = sp.TInt)
            
            )
        
            
    # @params : token_id, address
    @sp.entry_point
    
    def mintCertificate(self,params):
    
        
        sp.verify(~self.data.tokensMinted.contains(params.token_id))
        
        self.data.tokensMinted.add(params.token_id)
        
        sp.if ~self.data.ownerToBalance.contains(params.address):
            
            self.data.tokenHolderToID[params.address] = sp.set()
            
        sp.if ~self.data.addressToName.contains(sp.sender):
             
             self.data.addressToName[sp.sender]=params.name
            
        self.data.tokenHolderToID[params.address].add(params.token_id)
        
        self.data.tokenIDToScore[params.token_id] = params.score
        
        self.data.tokenIdToOwner[params.token_id] = params.address
        
        
        sp.if ~self.data.ownerToBalance.contains(params.address):
            
            self.data.ownerToBalance[params.address] = 0
            
        self.data.ownerToBalance[params.address] += 1
    
    
    # @params : token_id,
    @sp.entry_point
    
    def burnCertificate(self, params):
        
        sp.verify(sp.sender == self.data.admin)
        
        sp.verify(self.data.tokensMinted.contains(params.token_id))
        
        self.data.tokensMinted.remove(params.token_id)
        
        del self.data.tokenIdToOwner[params.token_id]
        
        del self.data.tokenIDToScore[params.token_id]
            
# Tests
@sp.add_test(name = "TezNFT Test")
def test():
    
    scenario = sp.test_scenario()
    scenario.h1("NFT Contract")

    
    admin = sp.test_account("Administrator")
    alice = sp.test_account("Alice")
    bob   = sp.test_account("Bob")
    robert = sp.test_account("Robert")
    dibs = sp.test_account("Dibyo")
    
    # Let's display the accounts:
    scenario.h2("Accounts")
    scenario.show([admin, alice, bob, robert,dibs])
    
    
    c1 = TezNFT("state","ST",admin.address)
    scenario += c1
    
    scenario.h2("Admin minting Tokens")
    scenario += c1.mintCertificate(token_id = "Kitty1", address = alice.address, name="Alice", score = 20).run(valid = True, sender = admin)
    scenario += c1.mintCertificate(token_id = "Kitty2", address = bob.address, name="Bob", score = 50).run(sender = admin)
    scenario += c1.mintCertificate(token_id = "Kitty3", address = bob.address, name="Bob", score = 20).run(sender = admin)
    scenario += c1.mintCertificate(token_id = "Kitty5", address = alice.address, name="Alice", score = 100).run(sender = admin)
    
    scenario += c1.burnCertificate(token_id = "Kitty2").run(valid= True, sender = admin)
