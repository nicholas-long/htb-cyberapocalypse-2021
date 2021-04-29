import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.*;
import javax.xml.validation.*;
import javax.xml.transform.stream.StreamSource;
import jakarta.servlet.*;
import jakarta.servlet.http.*;
import javax.xml.transform.dom.DOMResult;
import org.w3c.dom.Document;
import org.xml.sax.SAXException;
import java.util.*;
import java.util.stream.*;
import java.sql.*;
import java.io.*;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

public class Results extends HttpServlet {
   public void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException {
      Connection c = null;
      PreparedStatement stmt = null;
      String query = null;
      String body = request.getReader().lines().collect(Collectors.joining());
      PrintWriter out = response.getWriter();
      try {
         String xmlSchema = "request.xsd";
         SchemaFactory factory = SchemaFactory.newInstance("http://www.w3.org/2001/XMLSchema");
         Schema schema = factory.newSchema(new File(xmlSchema));
         factory.setProperty(XMLConstants.ACCESS_EXTERNAL_DTD, "file");
         factory.setProperty(XMLConstants.ACCESS_EXTERNAL_SCHEMA, "");
         Validator v = schema.newValidator();
         v.validate(new StreamSource(new StringReader(body)));
      }
      catch(SAXException | IOException e) {
         e.printStackTrace(out);
         return;
      }
      try {
         // create a new DocumentBuilder
         DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();

         // Make sekure!
         dbf.setXIncludeAware(false);
         dbf.setExpandEntityReferences(false);
         dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
         dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
         dbf.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false);
         dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
         dbf.setAttribute(XMLConstants.FEATURE_SECURE_PROCESSING, true);

         // Get query
         DocumentBuilder dBuilder = dbf.newDocumentBuilder();
         Document doc = dBuilder.parse(new ByteArrayInputStream(body.getBytes()));
         doc.getDocumentElement().normalize();
         query = doc.getFirstChild().getTextContent();

      } catch (Exception ex) {
         ex.printStackTrace(out);
      }

      try {
         // Query SQLite DB
         Class.forName("org.sqlite.JDBC");
         c = DriverManager.getConnection("jdbc:sqlite:airbase.db");
         c.setAutoCommit(false);

         stmt = c.prepareStatement("SELECT * from aircrafts where name like '%' || ? || '%'");
         stmt.setString(1, query);
         ResultSet rs = stmt.executeQuery();
         response.setContentType("application/json");
         out.print("[");
         while ( rs.next() ) {
            int id = rs.getInt("id");
            String  name = rs.getString("name");
            String url = rs.getString("url");
            String desc = rs.getString("description");
            String resp = String.format("{\"name\": \"%s\", \"url\":\"%s\", \"desc\":\"%s\"}, ", name, url, desc);
            out.print(resp);
         }
         out.print("{ \"name\" : \"\", \"url\" : \"\", \"desc\" : \"\" }]");
         rs.close();
         stmt.close();
         c.close();
      } catch ( Exception e ) {
         e.printStackTrace(out);
         return;
      }

   }
}
