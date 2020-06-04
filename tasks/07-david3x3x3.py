""" https://repl.it/@david3x3x3/advent7-2#main.py """

from itertools import permutations 

with open('07-input.txt') as fp: initprog = list(map(int, fp.readline().split(',')))
max = 0
for perm in permutations(range(5,10)):
  #print(perm)
  inps = [[phase] for phase in perm]
  progs = [list(initprog) for phase in perm]
  inps[0] += [0]
  running = [True]*5
  pcs = [0]*5
  while True in running: # wait for all progs to halt
    for cur_prog in range(5):
      prog = progs[cur_prog] # restore memory
      pc = pcs[cur_prog]     # restore program counter
      inp = inps[cur_prog]   # restore input
      while True:
        (x, cmd), args = divmod(prog[pc], 100), []
        for (i,iswrite) in enumerate([[],[0,0,1],[0,0,1],[1],[0],[0,0],[0,0],[0,0,1],[0,0,1]][cmd%99]):
          args += [prog[pc+i+1]]
          if x % 10 == 0 and iswrite == 0: args[-1] = prog[args[-1]]
          x //= 10
        orig_pc = pc
        if cmd == 1: prog[args[2]] = args[0] + args[1] # add
        elif cmd == 2: prog[args[2]] = args[0] * args[1] # multiply
        elif cmd == 3: # input
          if len(inp) == 0:
            break
          prog[args[0]] = inp.pop(0)
        elif cmd == 4: # output
          # add to the input of the next amp
          inps[(cur_prog+1)%5] += [args[0]]
          if cur_prog == 4:
            res = args[0]
        elif cmd == 5 and args[0] != 0: pc = args[1] # branch if true
        elif cmd == 6 and args[0] == 0: pc = args[1] # branch if false
        elif cmd == 7: prog[args[2]] = int(args[0] < args[1]) # test less than
        elif cmd == 8: prog[args[2]] = int(args[0] == args[1]) # test equal
        elif cmd == 99: # halt
          running[cur_prog] = False
          break
        if pc == orig_pc: pc += len(args) + 1 #only go to the next instruction if we didn't jump
      pcs[cur_prog] = pc # store program counter
  if res > max:
    max = res
    maxp = perm
print(max, maxp)