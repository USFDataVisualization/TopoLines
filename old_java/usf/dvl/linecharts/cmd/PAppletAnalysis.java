package usf.dvl.linecharts.cmd;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;

import processing.core.PApplet;
import processing.data.Table;
import processing.data.TableRow;
import usf.dvl.draw.DFrame;
import usf.dvl.draw.DPositionSet1D;
import usf.dvl.processing.PFrameApplet;
import usf.dvl.signal.Measures;

public class PAppletAnalysis extends PFrameApplet<DFrame> {

	HashMap<String,ArrayList<TableRow>> data = new HashMap<String,ArrayList<TableRow>>();

	public void setup() {
		super.setup();
		
		
		String outputFile = "/Users/prosen/allDatasets.csv";
		Table table = loadTable(outputFile, "header");
		
		for( int i = 0; i < table.getRowCount(); i++ ) {
			TableRow r = table.getRow(i);
			String title = r.getString("Data_file") + "_" +	r.getString("Filter_name");
			if( !data.containsKey(title) ) data.put( title, new ArrayList<TableRow>() );
			data.get(title).add(r);
		}
		
		for( String key : data.keySet() ) {
			ArrayList<TableRow> curr = data.get(key);
			System.out.println(key);
			analyze( curr, "L1Norm" );
			System.out.println();
		}
		
		
	}
	
	public void analyze( ArrayList<TableRow> curr, String field ) {
		curr.sort( new Comparator<TableRow>() {
			@Override public int compare(TableRow o1, TableRow o2) {
				if( o1.getFloat("Filter_Level") < o2.getFloat("Filter_Level") ) return -1;
				if( o1.getFloat("Filter_Level") > o2.getFloat("Filter_Level") ) return  1;
				return 0;
			}
		});
		Analysis clevel = new Analysis( curr, "Filter_Level" );
		Analysis cfield = new Analysis( curr, field );
		
		

		for( TableRow r : curr ) {
			System.out.println( r.getFloat("Filter_Level") + ": " + r.getFloat(field) );
		}
		System.out.println( "PCC: "+ Measures.getPearsonCorrelation(clevel, cfield) );
		
	}

	class Analysis implements DPositionSet1D {
		ArrayList<TableRow> rows;
		String field;
		Analysis( ArrayList<TableRow> _rows, String _field ){
			rows = _rows;
			field = _field;
		}
		@Override public int countPoints() { return rows.size(); }
		@Override public float getPoint(int idx) { return rows.get(idx).getFloat(field); }
		@Override public float getPointSize(int idx) { return 1; }
	}
	public static void main(String args[]) {
		PApplet.main(new String[] { "usf.dvl.linecharts.cmd.PAppletAnalysis" });
	}

}
