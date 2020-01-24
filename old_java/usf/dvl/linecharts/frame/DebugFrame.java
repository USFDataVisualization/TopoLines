package usf.dvl.linecharts.frame;

import processing.core.PApplet;
import usf.dvl.draw.DColorScheme;
import usf.dvl.draw.DMultiFrameGrid;
import usf.dvl.draw.frames.LineChartFrame;
import usf.dvl.signal.Signal;
import usf.dvl.signal.SignalDerivative;
import usf.dvl.signal.SignalDifference;
import usf.dvl.signal.filters.FilteredSignal;

public class DebugFrame extends DMultiFrameGrid<LineChartFrame> {

	Signal  orig;
	FilteredSignal          simp;
	SignalDifference diff;
	SignalDerivative orig_derv;
	SignalDerivative simp_derv;
	
	public DebugFrame(PApplet p, Signal _originalGraph, FilteredSignal _simp ) {
		super(p);
		
		orig = _originalGraph;
		simp = _simp;
		
		diff = new SignalDifference( orig, simp );
		
		orig_derv = new SignalDerivative( orig );
		simp_derv = new SignalDerivative( simp );
		
		for( int i = 0; i < 5; i++) {
			addFrame( new LineChartFrame(p) );
		}		
		
		getFrame(0).setData( orig );
		getFrame(1).setData( orig_derv );
		getFrame(2).setData( diff );
		getFrame(3).setData( simp );
		getFrame(4).setData( simp_derv );

		getFrame(0).setColorScheme( DColorScheme.Default.createStrokeOnly( p.color(  0,  0,  0), 1) );
		getFrame(1).setColorScheme( DColorScheme.Default.createStrokeOnly( p.color(255,  0,  0), 1) );
		getFrame(2).setColorScheme( DColorScheme.Default.createStrokeOnly( p.color(  0,255,  0), 1) );
		getFrame(3).setColorScheme( DColorScheme.Default.createStrokeOnly( p.color(  0,  0,255), 1) );
		getFrame(4).setColorScheme( DColorScheme.Default.createStrokeOnly( p.color(255,255,  0), 1) );
		
		/*
		float scale = getFrame(0).getMax() - getFrame(0).getMin();
		for( int i = 1; i <= 2; i++) {
			getFrame(i).overrideMinMax( getFrame(0).getMin(), getFrame(0).getMax() );
		}
		for( int i = 3; i < 5; i++) {
			getFrame(i).overrideMinMax( -scale/2, +scale/2 );
		}
		*/
		
	}

}

