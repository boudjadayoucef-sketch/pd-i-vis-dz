import { initializeApp, getApps, getApp } from "firebase/app";
import { 
  initializeFirestore,
  persistentLocalCache,
  persistentMultipleTabManager,
  collection, 
  doc, 
  getDocs, 
  setDoc, 
  updateDoc, 
  deleteDoc, 
  addDoc 
} from "firebase/firestore";
import { getAuth } from "firebase/auth";
import firebaseConfig from "../../firebase-applet-config.json";

// Allow the user to override Firebase configuration via client-side environment variables in AI Studio settings
const metaEnv = (import.meta as any).env || {};

const isCustomProject = !!(
  metaEnv.VITE_FIREBASE_API_KEY ||
  metaEnv.VITE_FIREBASE_PROJECT_ID
);

const activeConfig = {
  apiKey: metaEnv.VITE_FIREBASE_API_KEY || firebaseConfig.apiKey,
  authDomain: metaEnv.VITE_FIREBASE_AUTH_DOMAIN || firebaseConfig.authDomain,
  projectId: metaEnv.VITE_FIREBASE_PROJECT_ID || firebaseConfig.projectId,
  storageBucket: metaEnv.VITE_FIREBASE_STORAGE_BUCKET || firebaseConfig.storageBucket,
  messagingSenderId: metaEnv.VITE_FIREBASE_MESSAGING_SENDER_ID || firebaseConfig.messagingSenderId,
  appId: metaEnv.VITE_FIREBASE_APP_ID || firebaseConfig.appId,
  firestoreDatabaseId: isCustomProject
    ? (metaEnv.VITE_FIREBASE_DATABASE_ID || "")
    : (firebaseConfig.firestoreDatabaseId || "")
};

// Initialize Firebase
const app = getApps().length === 0 ? initializeApp(activeConfig) : getApp();

// Initialize Firestore with robust local offline persistence (IndexedDB)
const db = initializeFirestore(app, {
  localCache: persistentLocalCache({
    tabManager: persistentMultipleTabManager(),
  }),
}, activeConfig.firestoreDatabaseId || undefined);

const auth = getAuth(app);

export { db, auth, activeConfig };

// Interface for Plans (schemas)
export interface EngineeringPlan {
  id: string;
  title: string;
  fascicule: string;
  page: number;
  category: string;
  src: string;
  caption: string;
  tags: string[];
}

// Collection Names
const PLANS_COLLECTION = "plans";
const FASCICULES_COLLECTION = "fascicules_custom";

// --- Plans functions ---

// Fetch all plans
export async function fetchPlans(): Promise<EngineeringPlan[]> {
  try {
    const querySnapshot = await getDocs(collection(db, PLANS_COLLECTION));
    const plans: EngineeringPlan[] = [];
    querySnapshot.forEach((doc) => {
      plans.push({ id: doc.id, ...doc.data() } as EngineeringPlan);
    });
    return plans;
  } catch (error) {
    console.error("Error fetching plans from Firestore: ", error);
    throw error;
  }
}

// Add/Save plan
export async function savePlan(plan: Omit<EngineeringPlan, "id"> & { id?: string }): Promise<string> {
  try {
    if (plan.id) {
      await setDoc(doc(db, PLANS_COLLECTION, plan.id), plan);
      return plan.id;
    } else {
      const docRef = await addDoc(collection(db, PLANS_COLLECTION), plan);
      return docRef.id;
    }
  } catch (error) {
    console.error("Error saving plan to Firestore: ", error);
    throw error;
  }
}

// Delete plan
export async function deletePlanFromDb(id: string): Promise<void> {
  try {
    await deleteDoc(doc(db, PLANS_COLLECTION, id));
  } catch (error) {
    console.error("Error deleting plan from Firestore: ", error);
    throw error;
  }
}

// Seed plans if collection is empty
export async function seedPlansIfEmpty(defaultPlans: EngineeringPlan[]): Promise<void> {
  try {
    const querySnapshot = await getDocs(collection(db, PLANS_COLLECTION));
    if (querySnapshot.empty) {
      console.log("Seeding default plans into Firestore...");
      for (const plan of defaultPlans) {
        await setDoc(doc(db, PLANS_COLLECTION, plan.id), plan);
      }
    }
  } catch (error) {
    console.error("Error seeding plans: ", error);
  }
}

// Error handlers for standard formatting of Firestore Permission Errors
export enum OperationType {
  CREATE = 'create',
  UPDATE = 'update',
  DELETE = 'delete',
  LIST = 'list',
  GET = 'get',
  WRITE = 'write',
}

export interface FirestoreErrorInfo {
  error: string;
  operationType: OperationType;
  path: string | null;
  authInfo: {
    userId?: string | null;
    email?: string | null;
    emailVerified?: boolean | null;
    isAnonymous?: boolean | null;
    tenantId?: string | null;
    providerInfo?: {
      providerId?: string | null;
      email?: string | null;
    }[];
  }
}

export function handleFirestoreError(error: unknown, operationType: OperationType, path: string | null) {
  const errInfo: FirestoreErrorInfo = {
    error: error instanceof Error ? error.message : String(error),
    authInfo: {
      userId: auth.currentUser?.uid,
      email: auth.currentUser?.email,
      emailVerified: auth.currentUser?.emailVerified,
      isAnonymous: auth.currentUser?.isAnonymous,
      tenantId: auth.currentUser?.tenantId,
      providerInfo: auth.currentUser?.providerData?.map(provider => ({
        providerId: provider.providerId,
        email: provider.email,
      })) || []
    },
    operationType,
    path
  };
  console.error('Firestore Error: ', JSON.stringify(errInfo));
  throw new Error(JSON.stringify(errInfo));
}

export interface ProjectNotification {
  id?: string;
  projectId: string;
  projectName: string;
  message: string;
  category: "creation" | "update" | "assignment" | "status_change";
  authorName: string;
  authorEmail: string;
  authorRole?: string;
  timestamp: string;
  pole?: string;
  region?: string;
  readBy?: string[];
}

export async function createNotification(notif: Omit<ProjectNotification, "timestamp">): Promise<string> {
  try {
    const newNotif = {
      ...notif,
      timestamp: new Date().toISOString(),
      readBy: notif.readBy || []
    };
    const docRef = await addDoc(collection(db, "notifications"), newNotif);
    return docRef.id;
  } catch (error) {
    console.error("Error creating notification in Firestore:", error);
    throw error;
  }
}

