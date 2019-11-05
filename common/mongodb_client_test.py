# -*- coding: utf-8 -*-
import mongodb_client as client

# db.demo.find

def test():
    db = client.get_db('test')
    db.demo.drop()
    assert db.test.count == 0
    db.demo.insert({'test':123})
    assert db.demo.count() == 1
    db.demo.drop()
    assert db.demo.count == 0
    print 'test passed!'

if __name__ == "__main__":
    test()