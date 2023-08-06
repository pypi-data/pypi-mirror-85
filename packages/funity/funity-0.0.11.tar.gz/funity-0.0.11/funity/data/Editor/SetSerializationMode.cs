using UnityEditor;
using static funity.Utils;

namespace funity
{
    public static class SetSerializationMode
    {
        public static void ForceBinary()
        {
            Set(SerializationMode.ForceBinary);
        }

        public static void ForceText()
        {
            Set(SerializationMode.ForceText);
        }

        public static void Mixed()
        {
            Set(SerializationMode.Mixed);
        }

        private static void Set(SerializationMode serializationMode)
        {
            Log($"{nameof(SetSerializationMode)}.{serializationMode}");

            EditorSettings.serializationMode = serializationMode;

            Quit(EditorSettings.serializationMode == serializationMode);
        }
    }
}