package usf.dvl.linecharts.auto;

import java.io.IOException;
import java.util.ArrayList;

import processing.core.PApplet;
import processing.data.JSONObject;
import usf.dvl.common.MathX;
import usf.dvl.common.SystemX;
import usf.dvl.common.TaskExecutorService;
import usf.dvl.common.TaskExecutorService.Task;
import usf.dvl.signal.Measures;
import usf.dvl.signal.Signal;
import usf.dvl.signal.filters.DouglasPeuckerFilter;
import usf.dvl.signal.filters.FFTFilter;
import usf.dvl.signal.filters.FilteredSignal;
import usf.dvl.signal.filters.GaussianFilter;
import usf.dvl.signal.filters.MedianFilter;
import usf.dvl.signal.filters.PassThruFilter;
import usf.dvl.signal.filters.SubsampleFilter;
import usf.dvl.signal.filters.TDAFilter;

public class FilterInstance extends Task {

	public Class<? extends FilteredSignal> cls;
	public float filterLevel;
	public Signal 	originalGraph;
	public Signal 	originalGraphPhi;
	public FilteredSignal curData = null, curDataPhi = null;
	public String dataFile; 
	public String filterType;

	/*
	public static ArrayList<FilterInstance> procDataset( PApplet p, TaskExecutorService exec, String dataFile, int [] limit, float [] rate ) {
		ArrayList<FilterInstance> work = new ArrayList<FilterInstance>(); 
		try {

			Signal originalGraph = new Signal( p, SystemX.getResourceFile( dataFile ).getAbsolutePath() );
			Signal originalGraphPhi = new Signal( originalGraph );
			originalGraphPhi.remove(0);
			
			work.add( new FilterInstance( exec, dataFile, originalGraph, originalGraphPhi, PassThruFilter.class,	0 ) );
			for( int i = 1; i <= MathX.max(limit); i++ ) {
				if( i <= limit[0] ) work.add( new FilterInstance( exec, dataFile, originalGraph, originalGraphPhi, TDAFilter.class,		       rate[0]*i ) );
				if( i <= limit[1] ) work.add( new FilterInstance( exec, dataFile, originalGraph, originalGraphPhi, SubsampleFilter.class,      rate[1]*i ) );
				if( i <= limit[2] ) work.add( new FilterInstance( exec, dataFile, originalGraph, originalGraphPhi, FFTFilter.class,	  	       rate[2]*i ) );
				if( i <= limit[3] ) work.add( new FilterInstance( exec, dataFile, originalGraph, originalGraphPhi, MedianFilter.class,	       (float)Math.floor(rate[3]*i) ) );
				if( i <= limit[4] ) work.add( new FilterInstance( exec, dataFile, originalGraph, originalGraphPhi, GaussianFilter.class,       rate[4]*i ) );
				if( i <= limit[5] ) work.add( new FilterInstance( exec, dataFile, originalGraph, originalGraphPhi, DouglasPeuckerFilter.class, rate[5]*i ) );
			}	

		} catch (IOException e) {
			e.printStackTrace();
		}		
		return work;

	}
	*/
	
	private static float interp( float [] range, int cur, int tot ) {
		float f = MathX.map( cur, 0, tot-1, range[0], range[1]);
		return (float)Math.round(f*1000)/1000;
	}
	public static ArrayList<FilterInstance> procDataset( PApplet p, TaskExecutorService exec, String dataFile, int count, float [] tdaRange, float [] subRange, float [] fftRange, float [] medRange, float [] gauRange, float [] dpRange ) {
		ArrayList<FilterInstance> work = new ArrayList<FilterInstance>(); 
		try {

			Signal originalGraph = new Signal( p, SystemX.getResourceFile( dataFile ).getAbsolutePath() );
			Signal originalGraphPhi = new Signal( originalGraph );
			originalGraphPhi.remove(0);
			
			work.add( new FilterInstance( exec, dataFile, originalGraph, originalGraphPhi, PassThruFilter.class,	0 ) );
			for( int i = 0; i < count; i++ ) {
				work.add( new FilterInstance( exec, dataFile, originalGraph, originalGraphPhi, TDAFilter.class,		       interp( tdaRange, i, count) ) );
				work.add( new FilterInstance( exec, dataFile, originalGraph, originalGraphPhi, SubsampleFilter.class,      interp( subRange, i, count) ) );
				work.add( new FilterInstance( exec, dataFile, originalGraph, originalGraphPhi, FFTFilter.class,	  	       (float)Math.floor( interp( fftRange, i, count) ) ) );
				work.add( new FilterInstance( exec, dataFile, originalGraph, originalGraphPhi, MedianFilter.class,	       (float)Math.floor( interp( medRange, i, count) ) ) );
				work.add( new FilterInstance( exec, dataFile, originalGraph, originalGraphPhi, GaussianFilter.class,       interp( gauRange, i, count) ) );
				work.add( new FilterInstance( exec, dataFile, originalGraph, originalGraphPhi, DouglasPeuckerFilter.class, interp( dpRange, i, count) ) );
			}	
		} catch (IOException e) {
			e.printStackTrace();
		}		
		return work;

	}	

	public FilterInstance( TaskExecutorService exec, String _dataFile, Signal _originalGraph, Signal _originalGraphPhi, Class<? extends FilteredSignal> _cls, float _f ){
		super(exec);
		dataFile = _dataFile;
		originalGraph = _originalGraph;
		originalGraphPhi = _originalGraphPhi;
		filterLevel = _f;//Math.round(_f*10000)/10000;
		cls = _cls;
		if( cls == TDAFilter.class ) filterType = TDAFilter.filterType();
		if( cls == FFTFilter.class ) filterType = FFTFilter.filterType();
		if( cls == MedianFilter.class ) filterType = MedianFilter.filterType();
		if( cls == GaussianFilter.class ) filterType = GaussianFilter.filterType();
		if( cls == SubsampleFilter.class ) filterType = SubsampleFilter.filterType();
		if( cls == DouglasPeuckerFilter.class ) filterType = DouglasPeuckerFilter.filterType();
		if( cls == PassThruFilter.class ) filterType = PassThruFilter.filterType();
	}

	private void generate() {
		if( curData != null ) return;
		if( cls == TDAFilter.class ) { 
			curData    = new TDAFilter( originalGraph,    filterLevel );
			curDataPhi = new TDAFilter( originalGraphPhi, filterLevel );
		}
		if( cls == FFTFilter.class ) { 
			curData    = new FFTFilter( originalGraph,    (int) filterLevel );
			curDataPhi = new FFTFilter( originalGraphPhi, (int) filterLevel );
		}
		if( cls == MedianFilter.class ) { 
			curData    = new MedianFilter( originalGraph,    (int) filterLevel );
			curDataPhi = new MedianFilter( originalGraphPhi, (int) filterLevel );				
		}
		if( cls == GaussianFilter.class ) { 
			curData    = new GaussianFilter( originalGraph,    filterLevel );
			curDataPhi = new GaussianFilter( originalGraphPhi, filterLevel );					
		}
		if( cls == SubsampleFilter.class ) { 
			curData    = new SubsampleFilter( originalGraph,    filterLevel );
			curDataPhi = new SubsampleFilter( originalGraphPhi, filterLevel );				
		}
		if( cls == DouglasPeuckerFilter.class ) { 
			curData    = new DouglasPeuckerFilter( originalGraph,    filterLevel );
			curDataPhi = new DouglasPeuckerFilter( originalGraphPhi, filterLevel );				
		}				
		if( cls == PassThruFilter.class ) { 
			curData    = new PassThruFilter( originalGraph,    filterLevel );
			curDataPhi = new PassThruFilter( originalGraphPhi, filterLevel );				
		}				
	}


	@Override
	public void execute() {
		System.out.println("started " + dataFile + " (" + filterType + ": " + filterLevel +")" );
		generate();
		/*
		FilteredSignal f = curData;
		f.L1Norm();
		f.L2Norm();
		f.LInfNorm();
		f.frequencyPreservation();
		f.deltaVolume();
		f.peakinessBottleneck();
		f.peakinessWasserstein();
		*/
		toJSON();
	}	
	
	/*
	public String getImagePath() {
		return dataFile.replace(".json", "/") + filterType + "/" + "img-" + Float.toString(filterLevel).replace('.', '_') + ".png";
	}
	*/

	//public String getUID() { return dataFile + "_" + filterType + "_" + this.filterLevel; }

	JSONObject json = null;
	public JSONObject toJSON( ) {
		if( json != null ) return json;
		
		FilteredSignal f = curData;
		FilteredSignal fPhi = curDataPhi;

		JSONObject ret = new JSONObject();
		//ret.setString( "uid", getUID() );
		ret.setString( "datafile", dataFile );
		//ret.setString( "imagePath", getImagePath() );
		//ret.setString("filterType", f.graphType());
		ret.setString( "filterType", filterType );
		ret.setFloat( "filterLevel", f.getSimplificationLevel() );	
		//ret.setFloat("Filter_Percent", percent);	
		if( Float.isFinite(f.L1Norm()) ) ret.setFloat( "L1Norm", f.L1Norm() );	
		if( Float.isFinite(f.L2Norm()) ) ret.setFloat( "L2Norm", f.L2Norm() );	
		if( Float.isFinite(f.LInfNorm()) ) ret.setFloat("LInfNorm", f.LInfNorm() );	
		if( Float.isFinite(f.frequencyPreservation()) ) ret.setFloat( "frequencyPreservation", f.frequencyPreservation() );	
		if( Float.isFinite(f.deltaVolume()) ) ret.setFloat( "deltaVolume", f.deltaVolume() );	
		if( Float.isFinite(f.peakinessBottleneck()) ) ret.setFloat( "peakinessBottleneck", f.peakinessBottleneck() );	
		if( Float.isFinite(f.peakinessWasserstein()) ) ret.setFloat( "peakinessWasserstein", f.peakinessWasserstein() );	
		if( Float.isFinite(f.phaseShifted(fPhi)) ) ret.setFloat( "phaseShift", f.phaseShifted(fPhi) );
		if( Float.isFinite(f.signalToNoise()) ) ret.setFloat( "SNR", f.signalToNoise() );
		if( Double.isFinite(Measures.getSNR(f)) ) ret.setFloat( "SNRAlt", (float)Measures.getSNR(f) );
		if( Double.isFinite(Measures.approximateEntropy(f, 2, 0.25f)) ) ret.setFloat( "ent0_25", (float)Measures.approximateEntropy(f, 2, 0.25f) );
		if( Double.isFinite(Measures.approximateEntropy(f, 2, 0.50f)) ) ret.setFloat( "ent0_50", (float)Measures.approximateEntropy(f, 2, 0.50f) );
		if( Double.isFinite(Measures.approximateEntropy(f, 2, 1.00f)) ) ret.setFloat( "ent1_00", (float)Measures.approximateEntropy(f, 2, 1.00f) );
		if( Double.isFinite(Measures.approximateEntropy(f, 2, 2.00f)) ) ret.setFloat( "ent2_00", (float)Measures.approximateEntropy(f, 2, 2.00f) );
		if( Double.isFinite(Measures.approximateEntropy(f, 2, 4.00f)) ) ret.setFloat( "ent4_00", (float)Measures.approximateEntropy(f, 2, 4.00f) );
		ret.setJSONArray( "line", curData.signalJSON() );
		return (json=ret);
	}
	
	/*
	public JSONObject toSignalJSON( ) {
		generate();
		JSONObject ret = new JSONObject();
		ret.setString( "datafile", dataFile );
		ret.setJSONArray( "smoothLine", curData.signalJSON() );
		ret.setString( "filterType", filterType );
		ret.setFloat( "filterLevel", curData.getSimplificationLevel() );	
		return ret;
	}	
	 */

}
