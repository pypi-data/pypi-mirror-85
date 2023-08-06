import mage

##################################################
# USE CASE:  Create Assessment

print('\nCreating assessment...')
a = mage.Assessment.create('EXTERNAL', name='TEST')
print('Created assessment', a.name, a.id)

#BUG:  Assessment is not immediately findable
#while True:
#    print('\nFinding assessment...')
#    result = mage.Assessment.search(filter={'id': {'match': a.id}})
#    if len(result) > 0:
#        break

##################################################
# USE CASE:  List Assessment

for x in mage.Assessment.select('id', 'name').limit(5).list().auto_paging_iter():
    print(x.id, x.name)


##################################################
# USE CASE:  Find Assessment

print('\nFinding assessment...')
b = mage.Assessment.eq(id=a.id).search()[0]
print('Found assessment', b.name, b.id)

c = mage.Assessment.eq(name='TEST').search()
print("Found %d Assessments named 'TEST'" % len(c))


##################################################
# USE CASE:  Update Assessment Name

print('\nUpdating name to KILROY')
a.name = "KILROY"
print('Name is now', a.name)


##################################################
# USE CASE:  Start Assessment

print('\nStarting assessment')
run = a.start()
print(run)


##################################################
# USE CASE:  Delete Assessment

print('\nDeleting assessment')
a.delete()
