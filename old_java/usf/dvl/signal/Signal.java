package usf.dvl.signal;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.Vector;

import processing.core.PApplet;
import processing.data.JSONArray;
import processing.data.JSONObject;
import usf.dvl.draw.DPositionSet1D;

public class Signal implements DPositionSet1D, Iterable<Float> {

	private ArrayList<Float> data = new ArrayList<Float>();

	private float maxValue = -Float.MAX_VALUE;
	private float minValue =  Float.MAX_VALUE;

	public Signal( ) { }

	public Signal( Signal pc ) {
		for ( int i = 0; i < pc.countPoints(); i++ ) {
			addPoint( pc.getPoint(i) );
		}
	}

	public Signal( PApplet papplet, String filename ) {
		
		try {
			if( filename.toLowerCase().endsWith("json") ) { 
				JSONObject jsonObject = papplet.loadJSONObject(filename);
				JSONArray  nodeList   = null; 
				
				if( jsonObject.hasKey( "data" ) )    nodeList = jsonObject.getJSONArray("data");
				if( jsonObject.hasKey( "results" ) ) nodeList = jsonObject.getJSONArray("results");
				
				int limit = Integer.MAX_VALUE;
				for (int i = 0; i < nodeList.size() && i < limit; i++) {
					JSONObject jsnParse = nodeList.getJSONObject(i);
					addPoint( jsnParse.getFloat("value") );
				}
			}
			if( filename.toLowerCase().endsWith("csv") ) {
				BufferedReader reader = new BufferedReader(new FileReader( filename ));
				 String line;
				 while( ( line = reader.readLine() ) != null && this.size() < 2000 ) {
					 addPoint( Float.parseFloat(line) );
			     }
				 reader.close();
			}	

		} 
		catch(Exception e) {
			e.printStackTrace();
		}
	}
	

	public String graphType( ) {
		return "Original";
	}

	public void addPoint( float value ) {
		data.add( value );
		maxValue = Math.max(maxValue, value);
		minValue = Math.min(minValue, value);
	}

	
	public float getMinY() { 
		return minValue;
	}
	
	public float getMaxY() { 
		return maxValue;
	}

	public float interp( float x ) {
		if( x < 0 ) return data.get(0);
		if( x >= data.size()-1 ) return data.get( data.size()-1 );
		//return PApplet.map( x, (float)Math.floor(x), (float)Math.floor(x+1), get((int)x).value(), get((int)x+1).value() );
		return PApplet.map( x, (float)Math.floor(x), (float)Math.floor(x+1), data.get((int)x), data.get((int)x+1) );
	}

	public float get(int idx ) { return data.get(idx); }
	public int size() { return data.size(); }
	public void remove( int idx ) { data.remove(idx); }
	public void set( int idx, float val ) { data.set(idx, val); }

	@Override public int   countPoints() { return data.size(); }
	@Override public float getPoint(int idx) { return data.get(idx); }
	@Override public float getPointSize(int idx) { return 1; }
	

	@Override
	public Iterator<Float> iterator() { return data.iterator(); }

}
