package usf.dvl.signal;

public class SignalIntegral extends Signal {

	public SignalIntegral( Signal pc, float x0 ) {
		float cx = x0;
		addPoint(cx);
		for(int i = 0; i < pc.size(); i++ ) {
			cx += pc.get(i);
			addPoint( cx );
		}
	}

	
}
