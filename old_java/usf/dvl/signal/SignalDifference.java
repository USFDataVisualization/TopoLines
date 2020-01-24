package usf.dvl.signal;

public class SignalDifference extends Signal {

	public SignalDifference( Signal pc0, Signal pc1 ) {

		int i = 0;
		for( ; i < pc0.size() && i < pc1.size(); i++) {
			addPoint( pc0.get(i) - pc1.get(i) );
		}
		for( ; i < pc0.size(); i++) {
			addPoint( pc0.get(i) );
		}
		for( ; i < pc1.size(); i++) {
			addPoint( - pc1.get(i) );
		}
		
	}


}
