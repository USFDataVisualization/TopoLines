package usf.dvl.signal;

import usf.dvl.common.MathX;
import usf.dvl.draw.DPositionSet1D;

public class Measures {


	public static double getMean( DPositionSet1D data ){
		double sum = 0.0f;
		for(int i = 0; i < data.countPoints();i++){
			sum += data.getPoint(i);
		}
		return sum/data.countPoints();
	}

	public static double getStdevSample( DPositionSet1D data ){
		double mean = getMean(data);
		double var = 0.0f;
		for(int i=0; i< data.countPoints();i++){
			double value = data.getPoint(i);
			var += ((value - mean)*(value-mean));
		}
		return Math.sqrt( var/(data.countPoints()-1) );
	}  

	public static double getStdevPopulation( DPositionSet1D data ){
		double mean = getMean(data);
		double var = 0.0f;
		for(int i=0; i< data.countPoints();i++){
			double value = data.getPoint(i);
			var += ((value - mean)*(value-mean));
		}
		return Math.sqrt( var/(data.countPoints()) );
	}  


	public static double getSNR( DPositionSet1D data ) {
		return getMean(data) / getStdevSample(data);
	}
	
	public static double getVariance( DPositionSet1D data ) {
		return Math.pow( getStdevSample(data), 2 );
	}
	
	public static double getCovariance( DPositionSet1D d0, DPositionSet1D d1 ) {
		double m0 = getMean(d0);
		double m1 = getMean(d1);
		double covar = 0;
		for(int i= 0; i< d0.countPoints() && i < d1.countPoints(); i++){
			covar += (d0.getPoint(i) - m0)*(d1.getPoint(i)-m1);
		}
		return covar/ d0.countPoints();
	}
	
	public static double getPearsonCorrelation( DPositionSet1D d0, DPositionSet1D d1 ) {
		System.out.println( getCovariance( d0, d1 ) + " " + getStdevSample(d0) + " " + getStdevSample(d1) );
		return getCovariance( d0, d1 ) / ( getStdevPopulation(d0) * getStdevPopulation(d1) );
	}
	

	

	private static double approxEntMaxD( DPositionSet1D pc, int i, int j, int m ) {
		double maxD = 0;
		for( int k = 0; k < m; k++) {
			maxD = Math.max( maxD,  Math.abs(pc.getPoint(i+k)-pc.getPoint(j+k) ) );
		}
		return maxD;
	}
	
	private static double approxEntC( DPositionSet1D pc, int i, int m, double r ) {
		int cnt = 0;
		for( int j = 0; j < pc.countPoints()-m+1; j++ ) {
			double d = approxEntMaxD( pc, i, j, m );
			if( d < r ) cnt++;
		}
		return (double)cnt/(pc.countPoints()-m+1);
	}
	
	private static double approxEntPhi( DPositionSet1D pc, int m, double r ){
		
		double sum = 0;
		for( int i = 0; i < pc.countPoints()-m+1; i++ ) {
			double c = approxEntC( pc, i, m, r );
			sum += Math.log( c );
		}
		return sum/(pc.countPoints()-m+1);
	}
	
	public static double approximateEntropy( DPositionSet1D pc, int windowSize, double filterLevel ) {
		return approxEntPhi( pc, windowSize, filterLevel )-approxEntPhi( pc, windowSize+1, filterLevel );
	}
		
	
	
	// add all differences together
	public static double L1Norm( DPositionSet1D s0, DPositionSet1D s1 ) {
		double l1norm = 0;
		int i = 0;
		for(; i < s0.countPoints() && i < s1.countPoints(); i++ ){
			l1norm += Math.abs( s0.getPoint(i) - s1.getPoint(i) );
		}
		for(; i < s0.countPoints(); i++ ){
			l1norm += Math.abs( s0.getPoint(i) );
		}
		for(; i < s1.countPoints(); i++ ){
			l1norm += Math.abs( s1.getPoint(i) );
		}
		return l1norm;
	}

	
	// finds the area (euclidean distance)
	// iterates over all pairs of nodes without repeats or same-node pairs
	public static double L2Norm( DPositionSet1D s0, DPositionSet1D s1 ){
			double l2norm = 0;
			int i = 0;

			for(; i < s0.countPoints() && i < s1.countPoints(); i++ ){
				l2norm += MathX.sq( s0.getPoint(i) - s1.getPoint(i) );
			}
			for(; i < s0.countPoints(); i++ ){
				l2norm += MathX.sq( s0.getPoint(i) );
			}
			for(; i < s1.countPoints(); i++ ){
				l2norm += MathX.sq( s1.getPoint(i) );
			}

			l2norm = (double) Math.sqrt(l2norm);
		return l2norm;
	}

	// returns the absolute max y-value
	public static double LInfNorm( DPositionSet1D s0, DPositionSet1D s1 ){
		double linfnorm = -Double.POSITIVE_INFINITY;
		int i = 0;

		for(; i < s0.countPoints() && i < s1.countPoints(); i++ ){
			linfnorm = Math.max( linfnorm, Math.abs( s0.getPoint(i) - s1.getPoint(i) ) );
		}
		for(; i < s0.countPoints(); i++ ){
			linfnorm = Math.max( linfnorm, Math.abs( s0.getPoint(i) ) );
		}
		for(; i < s1.countPoints(); i++ ){
			linfnorm = Math.max( linfnorm, Math.abs( s1.getPoint(i) ) );
		}

		return linfnorm;
	}

	public static double deltaVolume( DPositionSet1D s0, DPositionSet1D s1 ) {
			double t0 = 0, t1 = 0;
			int i = 0;
			for(; i < s0.countPoints() && i < s1.countPoints(); i++ ){
				t0 += s0.getPoint(i);
				t1 += s1.getPoint(i);
			}
			for(; i < s0.countPoints(); i++ ){
				t0 += s0.getPoint(i);
			}
			for(; i < s1.countPoints(); i++ ){
				t1 += s1.getPoint(i);
			}
			
		return t1 - t0;
	}	
	
}
