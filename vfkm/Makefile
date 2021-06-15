# FLAGS=-g -Wall # debug
# FLAGS=-O2 -g -pg -Wall # profile
FLAGS=-O3 -Wall # release

main:
	g++ $(FLAGS) -o ../build/lib/dyntrack/vfkm main.cpp Vector.cpp PolygonalPath.cpp Vector2D.cc Util.cpp Grid.cpp Optimizer.cpp ConstraintMatrix.cpp -I.

clean:
	../DynTrack/vfkm
	rm *.o
