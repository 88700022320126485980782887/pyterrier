package org.terrier.python;
import static org.junit.Assert.*;

import java.net.URL;
import java.nio.file.Paths;
import java.util.Map;

import org.junit.Test;
import org.terrier.structures.indexing.DocumentPostingList;
public class TestJsonlPretok {

    @Test public void testIterator() throws Exception
    {
        URL resource = TestJsonlPretok.class.getResource("/test.jsonl");
        assertNotNull(resource);
        String testFilename = Paths.get(resource.toURI()).toFile().toString();
        JsonlPretokenisedIterator x = new JsonlPretokenisedIterator(testFilename); 
        assertTrue(x.hasNext());
        Map.Entry<Map<String,String>, DocumentPostingList> entry = x.next();
        assertEquals(entry.getKey().get("docno"), "d1");
        DocumentPostingList dpl = entry.getValue();
        assertEquals(dpl.getFrequency("a"), 1);
        assertEquals(dpl.getFrequency("b"), 40);
    }
}
