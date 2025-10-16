package main;

import com.google.gson.Gson;
import org.eclipse.jdt.core.dom.ASTNode;
import structure.*;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class RQ1_or {
	
	private class DATA {
		private List<String> filename;
		private List<String> codelines;
		private List<String> is_test_file;
		private List<String> file_label;
		private List<String> line_label;
		private List<String> line_number;
		private List<String> startLine;
		private List<String> endLine;
	}
	
	
	public static void main(String[] args) {
		String dir="E:\\Datasets\\preprocessed_data2";
//		File file = new File(dir);
//		String absolutePath = file.getAbsolutePath();
//		System.out.println("Absolute path: " + absolutePath);
		File fileDir=new File(dir);
		File[] FileList=fileDir.listFiles();
		for(File f:FileList) {
			try {
				BufferedReader reader=new BufferedReader(new FileReader(f));
				String release=f.getName();
				System.out.println("filename:"+release);
				String tempString;
				String outputpath="E:\\Datasets\\codewithast_2\\"+release;
				File outfile=new File(outputpath);
				File parentDir = outfile.getParentFile();
				if (!parentDir.exists() && !parentDir.mkdirs()) {
					throw new IllegalStateException("Couldn't create dir: " + parentDir.getAbsolutePath());
				}
				if(!outfile.exists()) {
					outfile.createNewFile();
				}
				OutputStream os=new FileOutputStream(outfile);
				System.out.println("filename:"+release);
				while((tempString=reader.readLine())!=null) {
					Gson gson=new Gson();
					DATA data=gson.fromJson(tempString, DATA.class);
					String code="";
					int num=data.codelines.size(),i=0;
					List[] ast=new List[num];

					
					for(String line:data.codelines) {
						code+=line+"\n";
						ast[i++]=new ArrayList();
					}
//					System.out.println(code);
					ASTGenerator astGenerator=new ASTGenerator(code);
					List<MyMethodNode> methodNodeList =astGenerator.getMethodNodeList();
					List<MyImportNode> importNodeList =astGenerator.getImportNodeList();
					List<MyPackageNode> packageNodeList =astGenerator.getPackageNodeList();
					List<MyTypeNode> typeNodeList =astGenerator.getTypeNodeList();
					List<MyAnnotationNode> annotationNodeList =astGenerator.getAnnotationNodeList();
					for(MyImportNode m:importNodeList) {
						ASTtoNodeType(m,ast);
					}
					
					for(MyPackageNode m:packageNodeList) {
						ASTtoNodeType(m,ast);
					}
					
					for(MyTypeNode m:typeNodeList) {
						ASTtoNodeType(m,ast);
					}
//					if(typeNodeList.size()>0) {
//						MyTypeNode m1=typeNodeList.get(0);
//						ASTtoNodeType(m1,ast);
//					}
					for(MyAnnotationNode m:annotationNodeList) {
						ASTtoNodeType(m,ast);
					}
//					if(annotationNodeList.size()>0) {
//						MyAnnotationNode m2=annotationNodeList.get(0);
//						ASTtoNodeType(m2,ast);
//					}
//					OUT out=new OUT(data.filename,data.codelines,data.is_test_file,data.file_label,data.line_label,data.line_number,ast);
//					String outString=gson.toJson(out)+"\n";
////					System.out.print(outString);
//
//					byte[] bytes=outString.getBytes("UTF-8");
//					os.write(bytes);

				}
				
				os.close();
			} catch (FileNotFoundException e) {
				
				e.printStackTrace();
			} catch (IOException e) {
				
				e.printStackTrace();
			}
//			System.out.println();
		}
	}
	
	@SuppressWarnings("unchecked")
	public static void ASTtoNodeType(MyAnnotationNode m, List[] data) {
		for(MyASTNode mn:m.nodeList) {
			String nodeType=ASTNode.nodeClassForType(mn.astNode.getNodeType()).getName().replace("org.eclipse.jdt.core.dom.", "");
			
			int startLine=mn.startLineNum;
			int endLine=mn.endLineNum;
			System.out.println("11:"+startLine);
            System.out.println("12:"+endLine);
			
			if (startLine<0)continue;
			
			if(nodeType.equals("Javadoc"))continue;
//			if(nodeType.equals("SimpleName")) {
//				System.out.println(mn.astNode.toString());
//				System.out.println(mn.astNode.getLength());
//			}
			for(int i=startLine;i<=endLine;i++) {
				
				data[i-1].add(nodeType);
				if(nodeType.equals("SimpleName")) {
					data[i-1].add(mn.astNode.toString());
				}
			}
		}
	}
	
	@SuppressWarnings("unchecked")
	public static void ASTtoNodeType(MyTypeNode m, List[] data) {
		for(MyASTNode mn:m.nodeList) {
			String nodeType=ASTNode.nodeClassForType(mn.astNode.getNodeType()).getName().replace("org.eclipse.jdt.core.dom.", "");
			
			int startLine=mn.startLineNum;
			int endLine=mn.endLineNum;
			System.out.println("21:"+startLine);
			System.out.println("22:"+endLine);
			
			if (startLine<0)continue;
			if(nodeType.equals("Javadoc"))continue;
//			if(nodeType.equals("SimpleName")) {
//				System.out.println(mn.astNode.toString());
//				System.out.println(mn.astNode.getLength());
//			}
			for(int i=startLine;i<=endLine;i++) {
//				System.out.println(i);
				data[i-1].add(nodeType);
				if(nodeType.equals("SimpleName")) {
					data[i-1].add(mn.astNode.toString());
				}
			}
		}
	}
	
	@SuppressWarnings("unchecked")
	public static void ASTtoNodeType(MyPackageNode m, List[] data) {
		for(MyASTNode mn:m.nodeList) {
			String nodeType=ASTNode.nodeClassForType(mn.astNode.getNodeType()).getName().replace("org.eclipse.jdt.core.dom.", "");
			
			int startLine=mn.startLineNum;
			int endLine=mn.endLineNum;
			System.out.println("31:"+startLine);
			System.out.println("32:"+endLine);
			
			if(nodeType.equals("Javadoc"))continue;
//			if(nodeType.equals("SimpleName")) {
//				System.out.println(mn.astNode.toString());
//				System.out.println(mn.astNode.getLength());
//			}
			for(int i=startLine;i<=endLine;i++) {
				data[i-1].add(nodeType);
				if(nodeType.equals("SimpleName")) {
					data[i-1].add(mn.astNode.toString());
				}
			}
		}
	}
	
	@SuppressWarnings("unchecked")
	public static void ASTtoNodeType(MyImportNode m, List[] data) {
		for(MyASTNode mn:m.nodeList) {
			String nodeType=ASTNode.nodeClassForType(mn.astNode.getNodeType()).getName().replace("org.eclipse.jdt.core.dom.", "");
			
			int startLine=mn.startLineNum;
			int endLine=mn.endLineNum;
			System.out.println("41:"+startLine);
			System.out.println("42:"+endLine);
			
			if(nodeType.equals("Javadoc"))continue;
//			if(nodeType.equals("SimpleName")) {
//				System.out.println(mn.astNode.toString());
//				System.out.println(mn.astNode.getLength());
//			}
			for(int i=startLine;i<=endLine;i++) {
				data[i-1].add(nodeType);
				if(nodeType.equals("SimpleName")) {
					data[i-1].add(mn.astNode.toString());
				}
			}
		}
	}
	
	@SuppressWarnings("unchecked")
	public static void ASTtoNodeType(MyMethodNode m, List[] data) {
		for(MyASTNode mn:m.nodeList) {
			String nodeType=ASTNode.nodeClassForType(mn.astNode.getNodeType()).getName().replace("org.eclipse.jdt.core.dom.", "");
			
			int startLine=mn.startLineNum;
			int endLine=mn.endLineNum;
			System.out.println("51:"+startLine);
			System.out.println("52:"+endLine);
			
			if(nodeType.equals("Javadoc"))continue;
//			if(nodeType.equals("SimpleName")) {
//				System.out.println(mn.astNode.toString());
//				System.out.println(mn.astNode.getLength());
//			}
			for(int i=startLine;i<=endLine;i++) {
				data[i-1].add(nodeType);
				if(nodeType.equals("SimpleName")) {
					data[i-1].add(mn.astNode.toString());
				}
			}
		}
	}
	
}

