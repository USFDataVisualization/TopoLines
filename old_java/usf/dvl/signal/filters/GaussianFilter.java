package usf.dvl.signal.filters;

import usf.dvl.signal.Signal;

public class GaussianFilter extends FilteredSignal {

	public GaussianFilter( Signal graph, float sd ) {
		super(graph,sd);
		int fw = (int)Math.max(1, Math.ceil(sd*3));
		float pi = (float) Math.PI;
		float SRtwoPi = (float) Math.sqrt(2*pi);
		float part_one = (float) (1/(sd*SRtwoPi));

		for ( int i = 0; i < graph.size(); i++ ) {
			float gaus = 0;
			float newval = 0;
			for ( int j = Math.max( 0, (int)(i-fw) ); j <= Math.min( i+fw, graph.size()-1 ); j++ ) {
				float val = (float)graph.get(j);
				double exponentOfE = Math.pow((j - i)/sd, 2);
				double exponentOfE2 = (-0.5) * exponentOfE;
				float part_two = (float)Math.exp( exponentOfE2 );

				/* Combine the equation */
				gaus += (float)part_one * part_two;
				newval += (float)part_one * part_two * val;
			}
			addPoint(newval/gaus);
		}
	}

	@Override public String graphType( ) {
		return filterType();
	}
	
	public static String filterType( ) {
		return "Gaussian";
	}
	
}
