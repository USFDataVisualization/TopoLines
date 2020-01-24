package usf.dvl.signal;

public class SignalDerivative extends Signal {

	public SignalDerivative( Signal pc ) {

		for( int i = 0; i < pc.size()-1; i++) {
			addPoint( pc.get(i+1) - pc.get(i) );
		}
	}


}
