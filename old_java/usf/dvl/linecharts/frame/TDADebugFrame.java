package usf.dvl.linecharts.frame;

import processing.core.PApplet;
import usf.dvl.draw.DColorScheme;
import usf.dvl.draw.DPositionSet2D;
import usf.dvl.draw.frames.LineChartFrame;
import usf.dvl.draw.frames.PointSetFrame;
import usf.dvl.signal.Signal;
import usf.dvl.signal.filters.TDAFilter;
import usf.saav.topology.merge.AbstractMergeTreeNode;

public class TDADebugFrame extends DebugFrame {

	public TDADebugFrame(PApplet p, Signal _originalGraph, TDAFilter _simp) {
		super(p, _originalGraph, _simp);
		
		clearFrames();

		for( int i = 0; i < 5; i++) {
			if( i == 0 ) 
				addFrame( new CPLineChart(p) );
			else if ( i == 1 ){
				addFrame( new DervLineChart(p) );
			}
			else
				addFrame( new LineChartFrame(p) );
		}		
		
		getFrame(0).setData( orig );
		getFrame(1).setData( orig_derv );
		getFrame(2).setData( diff );
		getFrame(3).setData( simp );
		getFrame(4).setData( simp_derv );

		/*
		getFrame(0).setColorScheme( DColorScheme.Default.createStrokeOnly( p.color(  0,  0,  0), 1) );
		getFrame(1).setColorScheme( DColorScheme.Default.createStrokeOnly( p.color(255,  0,  0), 1) );
		getFrame(2).setColorScheme( DColorScheme.Default.createStrokeOnly( p.color(  0,255,  0), 1) );
		getFrame(3).setColorScheme( DColorScheme.Default.createStrokeOnly( p.color(  0,  0,255), 1) );
		getFrame(4).setColorScheme( DColorScheme.Default.createStrokeOnly( p.color(255,255,  0), 1) );
		*/
				
	}
	
	class CPLineChart extends LineChartFrame {

		PointSetFrame psf;
		public CPLineChart(PApplet p) {
			super(p);
			psf = new PointSetFrame(p);
			psf.setData( new CPPositionData() );
			psf.setColorScheme( new CPColorScheme() );
		}
		
		@Override public void setPosition(int u0, int v0, int w, int h){
			super.setPosition(u0, v0, w, h);
			psf.setPosition(u0, v0, w, h);
		}
		
		@Override public void draw() {
			super.draw();
			psf.draw();
		}
		
		/*
		class CPPositionData implements DPositionSet2D {
			@Override public int countPoints() { return ((TDAFilter)simp).tt.size(); }
			@Override public float getPointX(int idx) { 
				int topo_idx = ((TDAFilter)simp).tt.getNode(idx).getID();
				float pos = ((TDAFilter)simp).topo.get(topo_idx).position();
				return PApplet.map( pos, 0, orig.countPoints(), 0, w); 
			} 
			@Override public float getPointY(int idx) { return PApplet.map( ((TDAFilter)simp).tt.getNode(idx).getValue(), orig.getMinY(), orig.getMaxY(), h, 0 ); }
			@Override public float getPointSize(int idx) { return 2; }
		}
		*/
		class CPPositionData implements DPositionSet2D {
			@Override public int countPoints() { return ((TDAFilter)simp).points.size(); }
			@Override public float getPointX(int idx) { 
				return PApplet.map(  ((TDAFilter)simp).points.get(idx).x, 0, orig.countPoints(), 0, w); 
			} 
			@Override public float getPointY(int idx) { 
				return PApplet.map( ((TDAFilter)simp).points.get(idx).y, orig.getMinY(), orig.getMaxY(), h, 0 ); 
			}
			@Override public float getPointSize(int idx) { return 2; }
		}		
		
		class CPColorScheme extends DColorScheme.Default {
			@Override public int getFill( int idx ) {
				AbstractMergeTreeNode node = ((TDAFilter)simp).tt.getNode(idx);
				if( node.getBirth() == node.getValue() ) return papplet.color(200,0,0);
				return papplet.color(0,0,200);
			}
		}
		
		
	}
	
	
	class DervLineChart extends LineChartFrame {

		PointSetFrame psf;
		public DervLineChart(PApplet p) {
			super(p);
			psf = new PointSetFrame(p);
			psf.setData( new CPPositionData() );
			psf.setColorScheme( new CPColorScheme() );
		}
		
		@Override public void setPosition(int u0, int v0, int w, int h){
			super.setPosition(u0, v0, w, h);
			psf.setPosition(u0, v0, w, h);
		}
		
		@Override public void draw() {
			super.draw();
			psf.draw();
		}
		
		/*
		class CPPositionData implements DPositionSet2D {
			@Override public int countPoints() { return ((TDAFilter)simp).tt.size(); }
			@Override public float getPointX(int idx) { 
				int topo_idx = ((TDAFilter)simp).tt.getNode(idx).getID();
				float pos = ((TDAFilter)simp).topo.get(topo_idx).position();
				return PApplet.map( pos, 0, orig.countPoints(), 0, w); 
			} 
			@Override public float getPointY(int idx) { return PApplet.map( ((TDAFilter)simp).tt.getNode(idx).getValue(), orig.getMinY(), orig.getMaxY(), h, 0 ); }
			@Override public float getPointSize(int idx) { return 2; }
		}
		*/
		class CPPositionData implements DPositionSet2D {
			@Override public int countPoints() { return ((TDAFilter)simp).points.size(); }
			@Override public float getPointX(int idx) { 
				return PApplet.map(  ((TDAFilter)simp).points.get(idx).x, 0, orig.countPoints(), 0, w); 
			} 
			@Override public float getPointY(int idx) { 
				return PApplet.map( 0, orig_derv.getMinY(), orig_derv.getMaxY(), h, 0 ); 
			}
			@Override public float getPointSize(int idx) { return 2; }
		}		
		
		class CPColorScheme extends DColorScheme.Default {
			@Override public int getFill( int idx ) {
				AbstractMergeTreeNode node = ((TDAFilter)simp).tt.getNode(idx);
				if( node.getBirth() == node.getValue() ) return papplet.color(200,0,0);
				return papplet.color(0,0,200);
			}
		}
		
		
	}
	

}
