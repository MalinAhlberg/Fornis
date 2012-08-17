# -*- python -*-
import sys
import cython
from libc.stdlib cimport malloc, free, realloc, calloc

cdef extern:
    int __builtin_clz (unsigned int)

ctypedef unsigned int weightint 
ctypedef unsigned short int ruleint 
ctypedef long long int hashint 
ctypedef unsigned int maskint 
ctypedef unsigned int chars_lengthint

cdef struct node:
    weightint weight
    maskint *usedchars 
    chars_lengthint usedchars_length 
    hashint anahash 
    ruleint sibling 
    ruleint child 
    weightint pweight 
    maskint *pusedchars 
    chars_lengthint pusedchars_length 
    hashint panahash

cdef struct pqi:
    node value
    pqi *next

cdef struct cpq:
    weightint current
    weightint size
    pqi **data


# COUNTER_pqi = [0]
# COUNTER_usedchars = [0]

cdef cpq *new_cpq(weightint size):
    cdef cpq *p = <cpq *>malloc(sizeof(cpq))
    p.data = <pqi **>calloc(sizeof(pqi *),size) # NB! calloc is important!
    p.size = size
    p.current = 0
    return p
    
cdef void free_cpq(cpq **p):   
    cdef pqi *i, *j
    cdef weightint k
    for k in range(p[0].current,p[0].size):
        i = p[0].data[k]
        while i:
            p[0].data[k] = i.next
            free(i.value.usedchars)
            free(i.value.pusedchars)
#            COUNTER_usedchars[0] -= 2
            free_pqi(&i)
            i = p[0].data[k]

    free(p[0].data)
    free(p[0])
    p[0] = NULL


cdef struct pqi_pool_t: 
    unsigned int grow_at
    pqi **content
    unsigned int length
cdef pqi_pool_t *pqi_pool = <pqi_pool_t *>malloc(sizeof(pqi_pool_t))
pqi_pool.grow_at = 1024 
pqi_pool.content = <pqi **>malloc(sizeof(pqi *)*pqi_pool.grow_at)
pqi_pool.length = 0
# NB! does not free .value.(p)usedchars or .next, only releases the node to the hot pool for reuse
cdef void free_pqi(pqi **i):
    # check to see if we must grow
    if pqi_pool.length == pqi_pool.grow_at:
        pqi_pool.grow_at *= 2
        pqi_pool.content = <pqi **>realloc(pqi_pool.content,sizeof(pqi *)*pqi_pool.grow_at)

    pqi_pool.content[pqi_pool.length] = i[0]
    pqi_pool.length += 1
    i[0] = NULL


cdef void free_pqi_pool():
    cdef unsigned int i
    for i in range(pqi_pool.length):
        free(pqi_pool.content[i])
#        COUNTER_pqi[0] -= 1
        pqi_pool.content[i] = NULL
    pqi_pool.length = 0


cdef pqi *alloc_pqi():
    cdef pqi *i

    if pqi_pool.length:
        pqi_pool.length -= 1
        i = pqi_pool.content[pqi_pool.length]
        pqi_pool.content[pqi_pool.length] = NULL

    else:
        i = <pqi *>malloc(sizeof(pqi))

#        COUNTER_pqi[0] += 1

    return i


cdef pqi *new_node_in_pqi(weightint weight,
                          maskint *usedchars, 
                          unsigned short int usedchars_length,
                          hashint anahash, 
                          ruleint sibling,
                          ruleint child,
                          weightint pweight, 
                          maskint *pusedchars, 
                          unsigned short int pusedchars_length,
                          hashint panahash):
    cdef pqi *i = alloc_pqi()
    i.next = NULL 
    i.value.weight = weight
    i.value.usedchars = usedchars
    i.value.usedchars_length = usedchars_length
    i.value.anahash = anahash
    i.value.sibling = sibling
    i.value.child = child
    i.value.pweight = pweight
    i.value.pusedchars = pusedchars
    i.value.pusedchars_length = pusedchars_length
    i.value.panahash = panahash

    return i


cdef bint forward_cpq(cpq *p):
    cdef weightint i
    if p.data[p.current]:
        return 1
    else:
        for i in range(p.current,p.size):
            if p.data[i]:
                p.current = i
                return 1
    return 0


cdef pqi *pop_cpq(cpq *p):
    cdef pqi *i = p.data[p.current]
    p.data[p.current] = i.next
    return i


cdef void push_cpq(cpq *p,weightint priority,pqi *i):
    i.next = p.data[priority]
    p.data[priority] = i


cdef struct maskint_pool_t: 
    unsigned int grow_at
    unsigned int length
    maskint **content

cdef maskint_pool_t *maskint_16_pool = <maskint_pool_t *>malloc(sizeof(maskint_pool_t))
maskint_16_pool.grow_at = 1024 
maskint_16_pool.content = <maskint **>malloc(sizeof(maskint *)*maskint_16_pool.grow_at)
maskint_16_pool.length = 0
cdef maskint_pool_t *maskint_64_pool = <maskint_pool_t *>malloc(sizeof(maskint_pool_t))
maskint_64_pool.grow_at = 1024 
maskint_64_pool.content = <maskint **>malloc(sizeof(maskint *)*maskint_64_pool.grow_at)
maskint_64_pool.length = 0
cdef maskint_pool_t *maskint_256_pool = <maskint_pool_t *>malloc(sizeof(maskint_pool_t))
maskint_256_pool.grow_at = 1024 
maskint_256_pool.content = <maskint **>malloc(sizeof(maskint *)*maskint_256_pool.grow_at)
maskint_256_pool.length = 0
cdef maskint_pool_t *maskint_1024_pool = <maskint_pool_t *>malloc(sizeof(maskint_pool_t))
maskint_1024_pool.grow_at = 1024 
maskint_1024_pool.content = <maskint **>malloc(sizeof(maskint *)*maskint_1024_pool.grow_at)
maskint_1024_pool.length = 0
cdef maskint_pool_t *maskint_4096_pool = <maskint_pool_t *>malloc(sizeof(maskint_pool_t))
maskint_4096_pool.grow_at = 256 
maskint_4096_pool.content = <maskint **>malloc(sizeof(maskint *)*maskint_4096_pool.grow_at)
maskint_4096_pool.length = 0


cdef void _free_maskint(maskint **i, maskint_pool_t *maskint_pool):
    if maskint_pool.length == maskint_pool.grow_at:
        maskint_pool.grow_at *= 2
        maskint_pool.content = <maskint **>realloc(maskint_pool.content,sizeof(maskint *)*maskint_pool.grow_at)

    maskint_pool.content[maskint_pool.length] = i[0]
    maskint_pool.length += 1
    i[0] = NULL

cdef void free_maskint(maskint **i,chars_lengthint length):
    cdef int bin = sizeof(chars_lengthint)*8-__builtin_clz(length)

    if bin == 12:
        _free_maskint(i,maskint_4096_pool)
    elif bin == 11:
        _free_maskint(i,maskint_4096_pool)
    if bin == 10:
        _free_maskint(i,maskint_1024_pool)
    elif bin == 9:
        _free_maskint(i,maskint_1024_pool)
    elif bin == 8:
        _free_maskint(i,maskint_256_pool)
    elif bin == 7:
        _free_maskint(i,maskint_256_pool)
    elif bin == 6:
        _free_maskint(i,maskint_64_pool)
    elif bin == 5:
        _free_maskint(i,maskint_64_pool)
    elif bin == 4:
        _free_maskint(i,maskint_16_pool)
    elif bin == 3:
        _free_maskint(i,maskint_16_pool)
    elif bin == 2:
        _free_maskint(i,maskint_16_pool)
    elif bin == 1:
        _free_maskint(i,maskint_16_pool)
    else:
        # not managed, just free it
        free(i[0])
        i[0] = NULL


cdef maskint *_alloc_maskint(maskint_pool_t *maskint_pool,chars_lengthint length):
    cdef maskint *i

    if maskint_pool.length:
        maskint_pool.length -= 1
        i = maskint_pool.content[maskint_pool.length]
        maskint_pool.content[maskint_pool.length] = NULL

    else:
        i = <maskint *>malloc(sizeof(maskint)*length)
#        if i == NULL:
#            print >>sys.stderr, 'No ALLOC!!'; sys.stderr.flush()

    return i

cdef maskint *alloc_maskint(chars_lengthint length):
    cdef int bin = sizeof(chars_lengthint)*8-__builtin_clz(length)
#    print >>sys.stderr,'alloc maskint', bin, length; sys.stderr.flush()
    if bin == 12:
        return _alloc_maskint(maskint_4096_pool,4096)
    elif bin == 11:
        return _alloc_maskint(maskint_4096_pool,4096)
    elif bin == 10:
        return _alloc_maskint(maskint_1024_pool,1024)
    elif bin == 9:
        return _alloc_maskint(maskint_1024_pool,1024)
    elif bin == 8:
        return _alloc_maskint(maskint_256_pool,256)
    elif bin == 7:
        return _alloc_maskint(maskint_256_pool,256)
    elif bin == 6:
        return _alloc_maskint(maskint_64_pool,64)
    elif bin == 5:
        return _alloc_maskint(maskint_64_pool,64)
    elif bin == 4:
        return _alloc_maskint(maskint_16_pool,16)
    elif bin == 3:
        return _alloc_maskint(maskint_16_pool,16)
    elif bin == 2:
        return _alloc_maskint(maskint_16_pool,16)
    elif bin == 1:
        return _alloc_maskint(maskint_16_pool,16)
    else:
#        print >>sys.stderr, 'unmanagaded'; sys.stderr.flush()
        # not managed, just _alloc it
        return <maskint *>malloc(sizeof(maskint)*length)

    



cdef struct rule:
    weightint cost
    hashint delta_anahash
    maskint *neededchars
    unsigned short int neededchars_length


cdef void nextpossiblerule(ruleint in_child, 
                           maskint *in_usedchars, unsigned short int in_usedchars_length, 
                           rule *rules, unsigned short int rules_length, 
                           weightint max_cost, 
                           # output args
                           ruleint *out_child, 
                           maskint **out_usedchars, unsigned short int *out_usedchars_length):
    
    cdef ruleint i=0
    cdef chars_lengthint j=0, k=0, possible=0

    # count from current rule to end of rule list
    for i in range(in_child,rules_length): 
        if rules[i].cost >= max_cost:
            break
 
        for j in range(0,in_usedchars_length):
            for k in range(0,rules[i].neededchars_length):
                if not rules[i].neededchars[k]&in_usedchars[j]:
                    possible += 1
        
        if possible:
#            print >>sys.stderr, ' npr pos', possible
#            sys.stderr.flush()
            out_usedchars_length[0] = possible 
            out_usedchars[0] = alloc_maskint(possible)            
#            COUNTER_usedchars[0] += 1
            out_child[0] = i

            
            possible = 0
            for j in range(0,in_usedchars_length):
                for k in range(0,rules[i].neededchars_length):
                    if not rules[i].neededchars[k]&in_usedchars[j]:
                        out_usedchars[0][possible] = rules[i].neededchars[k]|in_usedchars[j]
                        possible += 1

            return
        
    out_usedchars[0] = NULL
    out_usedchars_length[0] = 0
    out_child[0] = 0
    return


# generator to be called from python
def dijkstrafind(py_rules,hashint anahash,_,weightint th):

    cdef unsigned short int i,j,
    cdef long long int iters 
    cdef chars_lengthint neededchars_length 
    cdef ruleint npr_child 
    cdef maskint *npr_usedchars
    cdef unsigned short int npr_usedchars_length
    cdef pqi *v_in_pqi
    cdef node *v
    cdef weightint weight

    # copy over the rules to c-space
#    print >>sys.stderr, '# copy over the rules to c-space'
#    sys.stderr.flush()
    cdef unsigned short int rules_length = len(py_rules)
    cdef rule *rules = <rule *>malloc(sizeof(rule)*rules_length)
    for i in range(rules_length):
        rules[i].delta_anahash = py_rules[i][0]
        rules[i].cost = py_rules[i][1]
        rules[i].neededchars_length = len(py_rules[i][2])

    neededchars_length = 0
    for i in range(rules_length):
        neededchars_length += rules[i].neededchars_length
    cdef maskint *neededchars = alloc_maskint(neededchars_length)
    for i in range(rules_length):
        rules[i].neededchars = neededchars
        for j in range(rules[i].neededchars_length):
            rules[i].neededchars[j] = py_rules[i][2][j]
        neededchars += rules[i].neededchars_length
    neededchars = rules[0].neededchars
            



    # setup the priority queue and push the first node
#    print >>sys.stderr, '# setup the priority queue and push the first node'
#    sys.stderr.flush()

    cdef cpq *pq = new_cpq(th+1)
    push_cpq(pq,0,new_node_in_pqi(0,                                            # weight
                                     <maskint *>calloc(16,sizeof(maskint)),     # usedchars
                                     1,                                         # usedchars_length 
                                     anahash,                                   # anahash
                                     len(py_rules),                             # sibling  
                                     0,                                         # child 
                                     0,                                         # pweight 
                                     <maskint *>calloc(16,sizeof(maskint)),      # pusedchars
                                     0,                                         # pusedchars_length 
                                     0))                                        # panahash

#    COUNTER_usedchars[0] += 2

    # read out the priority queue until empty or upstairs raises GeneratorExit
#    print >>sys.stderr, '# read out the priority queue until empty or upstairs raises GeneratorExit'
#    sys.stderr.flush()



    iters = 1 # 1 for start node
    while forward_cpq(pq):

#        print >>sys.stderr, 'pop'
#        sys.stderr.flush()

        v_in_pqi = pop_cpq(pq)
        v = &(v_in_pqi.value)

        try:
            yield (v.anahash,v.weight,iters)
#            print >>sys.stderr, ' ', v.anahash, v.weight, v.usedchars==NULL, v.usedchars_length, v.sibling, v.child, v.pweight, v.pusedchars==NULL, v.pusedchars_length, v.panahash
#            sys.stderr.flush()

        except GeneratorExit:
            break
        iters += 1


    # check for siblings
#        print >>sys.stderr, '# check for siblings'
#        sys.stderr.flush()

#        print >>sys.stderr, ' npr'
#        sys.stderr.flush()
        nextpossiblerule(v.sibling, v.pusedchars, v.pusedchars_length, rules, rules_length, th-v.pweight, &npr_child, &npr_usedchars, &npr_usedchars_length)
#        print >>sys.stderr, ' done'
#        sys.stderr.flush()

        if npr_usedchars_length:
            weight = rules[npr_child].cost + v.pweight
            push_cpq(pq,weight,new_node_in_pqi(weight,
                                                  npr_usedchars,
                                                  npr_usedchars_length,
                                                  rules[npr_child].delta_anahash + v.panahash,
                                                  npr_child+1,
                                                  npr_child,
                                                  v.pweight,
                                                  v.pusedchars,
                                                  v.pusedchars_length,
                                                  v.panahash))
        else:
            # No more siblings: free some parent data
#            print >>sys.stderr, '# No more siblings: free some parent data'
#            sys.stderr.flush()
            free_maskint(&v.pusedchars,v.pusedchars_length)
#            COUNTER_usedchars[0] -= 1

        # check for children
#        print >>sys.stderr, '# check for children'
#        sys.stderr.flush()


#        print >>sys.stderr, ' npr'
#        sys.stderr.flush()
        nextpossiblerule(v.child, v.usedchars, v.usedchars_length, rules, rules_length, th-v.weight, &npr_child, &npr_usedchars, &npr_usedchars_length)
#        print >>sys.stderr, ' done'
#        sys.stderr.flush()


        if npr_usedchars_length:
            weight = rules[npr_child].cost + v.weight
            push_cpq(pq,weight,new_node_in_pqi(weight,
                                                  npr_usedchars,
                                                  npr_usedchars_length,
                                                  rules[npr_child].delta_anahash + v.anahash,
                                                  npr_child+1,
                                                  npr_child,
                                                  v.weight,
                                                  v.usedchars,
                                                  v.usedchars_length,
                                                  v.anahash))
        else:
            # No more childrens: free some data
#            print >>sys.stderr, '# No more children: free some data'
#            sys.stderr.flush()
            free_maskint(&v.usedchars,v.usedchars_length)
#            COUNTER_usedchars[0] -= 1

        # return this pqi to the pool
#        print >>sys.stderr, '# return this pqi to the pool'
#        sys.stderr.flush()
        free_pqi(&v_in_pqi)


    if v_in_pqi:
        free_maskint(&v.usedchars,v.usedchars_length)
        free_maskint(&v.pusedchars,v.pusedchars_length)
        free_pqi(&v_in_pqi)
    free_maskint(&neededchars,neededchars_length)
    free(rules)
    rules = NULL
    free_cpq(&pq)
#    free_pqi_pool()
#    print pqi_pool.grow_at, pqi_pool.length

#    print 'pqi', COUNTER_pqi[0], 'usedchars', COUNTER_usedchars[0]
       
 









