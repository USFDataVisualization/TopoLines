package usf.dvl.linecharts.cmd;

import java.io.IOException;

import processing.core.PApplet;
import usf.dvl.common.SystemX;
import usf.dvl.draw.DMultiFrameGrid;
import usf.dvl.linecharts.frame.DebugFrame;
import usf.dvl.linecharts.frame.SideBySideFrame;
import usf.dvl.linecharts.frame.TDADebugFrame;
import usf.dvl.processing.PFrameApplet;
import usf.dvl.signal.Signal;
import usf.dvl.topology.distance.HeraTopologicalDistance;

public class PAppletMain extends PFrameApplet<DMultiFrameGrid<?>> {


	//String dataFile = "/climateData/t13-14.json";
	//String dataFile = "/radioAstronomy/output_122_128.json";
	String dataFile = "/stock/amzn.json";
	//String dataFile = "/stock/appl.json";
	//String dataFile = "/climate/avgTemp.json";
	//String dataFile = "/climate/contiguousPerception.json";
	//String dataFile = "/climate/DroughtSevIndx1901_2000.json";
	//String dataFile = "/statistical/amzn_price.json";
	

	public static float tdaSimplificationThreshold = 0;
	public static float guassianStdev = 0.25f;
	public static float subsampleRate = 1;
	public static float dpSimp = 0;
	public static int   medianWidth = 1;
	public static int   rfftMin = 0, rfftMax = 2000;
	
	Signal 	originalGraph;
	
	SideBySideFrame acf;
	DebugFrame debug = null;

	public PAppletMain() {
		super( 1200, 700, true );
	}

	public void setup(){
		super.setup();
		
		HeraTopologicalDistance.wasserstein_dist_path = "/Users/prosen/Code/usfdvl-topology/tda/hera/wasserstein_dist.mac";
		HeraTopologicalDistance.bottleneck_dist_path  = "/Users/prosen/Code/usfdvl-topology/tda/hera/bottleneck_dist.mac";
		
		try {
			originalGraph = new Signal( this, SystemX.getResourceFile( dataFile ).getAbsolutePath() );
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		acf = new SideBySideFrame( this, originalGraph );
		setFrame( acf );
	}

	
	@Override
	public void keyPressed() {
		super.keyPressed();
		switch( key ) {
		case 's': saveSVG(); break;
		case '1': setFrame( acf ); break;
		case '2': debug = new TDADebugFrame( this, originalGraph, acf.tdaFilterGraph );       setFrame(debug); break;
		case '3': debug = new DebugFrame(    this, originalGraph, acf.subsampleFilterGraph ); setFrame(debug); break;
		case '4': debug = new DebugFrame(    this, originalGraph, acf.rfftFilterGraph );      setFrame(debug); break;
		case '5': debug = new DebugFrame(    this, originalGraph, acf.medianFilterGraph );    setFrame(debug); break;
		case '6': debug = new DebugFrame(    this, originalGraph, acf.gaussianFilterGraph );  setFrame(debug); break;
		case '7': debug = new DebugFrame(    this, originalGraph, acf.dpFilterGraph );  	  setFrame(debug); break;
		}
	}


	public static void main(String args[]) {
		PApplet.main(new String[] { "usf.dvl.linecharts.cmd.PAppletMain" });
	}


}


