package usf.dvl.linecharts.frame;

import processing.core.PApplet;
import usf.dvl.draw.DMultiFrameGrid;
import usf.dvl.linecharts.cmd.PAppletMain;
import usf.dvl.signal.Measures;
import usf.dvl.signal.Signal;
import usf.dvl.signal.filters.DouglasPeuckerFilter;
import usf.dvl.signal.filters.FFTFilter;
import usf.dvl.signal.filters.FilteredSignal;
import usf.dvl.signal.filters.GaussianFilter;
import usf.dvl.signal.filters.MedianFilter;
import usf.dvl.signal.filters.SubsampleFilter;
import usf.dvl.signal.filters.TDAFilter;

public class SideBySideFrame extends DMultiFrameGrid<LineChart> {

	Signal 	originalGraph;
	public TDAFilter 			tdaFilterGraph;
	public FFTFilter 			rfftFilterGraph;
	public MedianFilter 		medianFilterGraph;
	public GaussianFilter 		gaussianFilterGraph;
	public SubsampleFilter		subsampleFilterGraph;
	public DouglasPeuckerFilter dpFilterGraph;

	
	public SideBySideFrame(PApplet p, Signal _originalGraph ) {
		super(p);
		
		originalGraph = _originalGraph;
		tdaFilterGraph   	 = new TDAFilter(originalGraph, PAppletMain.tdaSimplificationThreshold);
		subsampleFilterGraph = new SubsampleFilter( originalGraph, PAppletMain.subsampleRate );
		rfftFilterGraph   	 = new FFTFilter( originalGraph, PAppletMain.rfftMax );
		medianFilterGraph    = new MedianFilter( originalGraph, PAppletMain.medianWidth );
		gaussianFilterGraph  = new GaussianFilter( originalGraph, PAppletMain.guassianStdev );
		dpFilterGraph		 = new DouglasPeuckerFilter( originalGraph, PAppletMain.dpSimp );
		
		for( int i = 0; i < 7; i++) {
			addFrame( new LineChart(p) );
		}		
		
		getFrame(0).setData( originalGraph, originalGraph );        // Original graph
		getFrame(1).setData( originalGraph, tdaFilterGraph );    // TDA simplification
		getFrame(2).setData( originalGraph, subsampleFilterGraph ); // Every other point
		getFrame(3).setData( originalGraph, rfftFilterGraph );    // RFFT
		getFrame(4).setData( originalGraph, medianFilterGraph );
		getFrame(5).setData( originalGraph, gaussianFilterGraph );   // Gaussian
		getFrame(6).setData( originalGraph, dpFilterGraph );   
			
	}
	
	
	@Override public void draw() {
		super.draw();
		

		papplet.stroke(0);
		papplet.fill(0);
		for( LineChart f : getFrames() ) {
			LineChart lc = ((LineChart)f);
			if( lc.points instanceof FilteredSignal ) {
				FilteredSignal fs = (FilteredSignal)lc.points;
				float curV = lc.getV0()+30;
				papplet.text( "Simplification Level:" + fs.getSimplificationLevel(), lc.getU0()+10, curV ); curV += 15;
				papplet.text( "L-1:   " + fs.L1Norm(),      lc.getU0()+10, curV ); curV += 15;
				papplet.text( "L-2:   " + fs.L2Norm(),      lc.getU0()+10, curV ); curV += 15;
				papplet.text( "L-Inf: " + fs.LInfNorm(),    lc.getU0()+10, curV ); curV += 15;
				papplet.text( "dVol:  " + fs.deltaVolume(), lc.getU0()+10, curV ); curV += 15;
				papplet.text( "Peakiness Bottleneck:" + fs.peakinessBottleneck(), lc.getU0()+10, curV ); curV += 15;
				papplet.text( "Peakiness Wasserstein: " + fs.peakinessWasserstein(), lc.getU0()+10, curV ); curV += 15;
				papplet.text( "Frequency Preservation: " + fs.frequencyPreservation(), lc.getU0()+10, curV ); curV += 15;
				//papplet.text( "Phase Shift: " + f.phaseShifted(curDataPhi), lc.getU0()+10, curV ); curV += 15;
				papplet.text( "SNR: " + fs.signalToNoise(), lc.getU0()+10, curV ); curV += 15;
				papplet.text( "SNRAlt: " + Measures.getSNR(fs), lc.getU0()+10, curV ); curV += 15;
				papplet.text( "Ent0_25: " + Measures.approximateEntropy(fs, 2, 0.25f), lc.getU0()+10, curV ); curV += 15;
				papplet.text( "Ent0_50: " + Measures.approximateEntropy(fs, 2, 0.50f), lc.getU0()+10, curV ); curV += 15;
				papplet.text( "Ent1_00: " + Measures.approximateEntropy(fs, 2, 1.00f), lc.getU0()+10, curV ); curV += 15;
				papplet.text( "Ent2_00: " + Measures.approximateEntropy(fs, 2, 2.00f), lc.getU0()+10, curV ); curV += 15;
				papplet.text( "Ent4_00: " + Measures.approximateEntropy(fs, 2, 4.00f), lc.getU0()+10, curV ); curV += 15;
				
			}
		}
				
	}

	@Override
	public boolean keyPressed(){
		if( getFrame(1).hovered ){
			//if( papplet.key == '+' ) { MainViewer.tdaSimplificationThreshold += 0.15; }
			//if( papplet.key == '-' ) { MainViewer.tdaSimplificationThreshold -= 0.15; }
			if( papplet.key == '+' ) { PAppletMain.tdaSimplificationThreshold += 0.1; }
			if( papplet.key == '-' ) { PAppletMain.tdaSimplificationThreshold -= 0.1; }
			PAppletMain.tdaSimplificationThreshold = PApplet.constrain(PAppletMain.tdaSimplificationThreshold, 0, Float.MAX_VALUE );
			tdaFilterGraph = new TDAFilter(originalGraph, PAppletMain.tdaSimplificationThreshold);
			getFrame(1).setData( originalGraph, tdaFilterGraph );    // TDA simplification
			return true;
		}
		if( getFrame(2).hovered ){
			if( papplet.key == '+' ) { PAppletMain.subsampleRate += 0.5; }
			if( papplet.key == '-' ) { PAppletMain.subsampleRate -= 0.5; }
			subsampleFilterGraph = new SubsampleFilter( originalGraph, PAppletMain.subsampleRate );
			getFrame(2).setData( originalGraph, subsampleFilterGraph ); // Every other point
			return true;
		}
		if( getFrame(3).hovered ){
			if( papplet.key == '+' ) { PAppletMain.rfftMax += 5; }
			if( papplet.key == '-' ) { PAppletMain.rfftMax -= 5; }
			rfftFilterGraph = new FFTFilter( originalGraph, PAppletMain.rfftMax );
			getFrame(3).setData( originalGraph, rfftFilterGraph );    // RFFT
			return true;
		}  
		if( getFrame(4).hovered ){
			if( papplet.key == '+' ) { PAppletMain.medianWidth += 1; }
			if( papplet.key == '-' ) { PAppletMain.medianWidth = Math.max(1,PAppletMain.medianWidth-1); }
			medianFilterGraph = new MedianFilter( originalGraph, PAppletMain.medianWidth );
			getFrame(4).setData( originalGraph, medianFilterGraph );
			return true;
		}
		if( getFrame(5).hovered ){
			if( papplet.key == '+' ) { PAppletMain.guassianStdev += 0.25; }
			if( papplet.key == '-' ) { PAppletMain.guassianStdev -= 0.25; }
			gaussianFilterGraph = new GaussianFilter( originalGraph, PAppletMain.guassianStdev );
			getFrame(5).setData( originalGraph, gaussianFilterGraph );   // Gaussian
			return true;
		}
		if( getFrame(6).hovered ){
			if( papplet.key == '+' ) { PAppletMain.dpSimp += 0.1; }
			if( papplet.key == '-' ) { PAppletMain.dpSimp -= 0.1; }
			dpFilterGraph = new DouglasPeuckerFilter( originalGraph, PAppletMain.dpSimp );
			getFrame(6).setData( originalGraph, dpFilterGraph );   // Gaussian
			return true;
		}
		return false;		
	}	
	


}
